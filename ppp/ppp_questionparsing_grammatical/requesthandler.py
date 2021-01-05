"""Request handler of the module."""

import json
import pickle
import hashlib
import random
import logging
import requests

# Import pylibmc if possible; import memcache otherwise.
# pylibmc is is more strict (ie. detects and raises errors instead
# of just ignoring them), but is not compatible with Pypy.
try:
    import pylibmc as memcache
except ImportError:
    try:
        import memcache
    except ImportError:
        raise ImportError('Neither pylibmc or python3-memcached is installed')

from ppp_datamodel import Sentence, Resource, List
from ppp_datamodel.communication import TraceItem, Response
from ppp_libmodule.exceptions import ClientError

from .config import Config
from . import computeTree, simplify, normalFormProduction, QuotationHandler,\
    QuotationError, NamedEntityMerging, PrepositionMerging

def connect_memcached():
    mc = memcache.Client(Config().memcached_servers)
    return mc

class StanfordNLP:
    def __init__(self, urls):
        self.servers = urls

    def _parse(self, text):
        '''
            Need to run CoreNLP server with version > 3.6.0.
            See http://stackoverflow.com/questions/36206407/utf-8-issue-with-corenlp-server
        '''
        server = random.choice(self.servers)
        r = requests.post(server, params={'properties' : '{"annotators": "tokenize,ssplit,pos,lemma,ner,parse", "outputFormat": "json", "parse.flags": " -makeCopulaHead"}'}, data=text.encode('utf8'))
        result = r.json()['sentences'][0]
        result['text'] = text
        return result

    def parse(self, text):
        """Perform a query to all configured APIs and concatenates all
        results into a single list.
        Also handles caching."""
        mc = connect_memcached()

        # Construct a key suitable for memcached (ie. a string of less than
        # 250 bytes) with a salt (to prevent attacks by hash collision)
        salt = Config().memcached_salt
        key = hashlib.md5((salt + text).encode()).hexdigest()
        key = 'ppp-qp-grammatical-%s' + key

        # Get the cached value, if any
        r = mc.get(key)
        if not r:
            # If there is no cached value, compute it.
            r = self._parse(text)
            mc.set(key, pickle.dumps(r), time=Config().memcached_timeout)
        else:
            r = pickle.loads(r)
        return r
stanfordnlp = StanfordNLP(Config().corenlp_servers)

def parse(sentence):
    handler = QuotationHandler()
    nonAmbiguousSentence = handler.pull(sentence)
    result = stanfordnlp.parse(nonAmbiguousSentence)
    tree = computeTree(result)
    handler.push(tree)
    NamedEntityMerging(tree).merge()
    PrepositionMerging(tree).merge()
    qw = simplify(tree)
    return normalFormProduction(tree, qw)

class RequestHandler:
    __slots__ = ('request', )
    def __init__(self, request):
        self.request = request

    def answer(self):
        if not isinstance(self.request.tree, Sentence) or \
                self.request.language != 'en':
            return []
        sentence = self.request.tree.value
        try:
            tree = parse(sentence)
        except QuotationError: # no logging, the error is between the chair and the keyboard
            return []
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.warning(e)
            return []
        if isinstance(tree, (Resource, List)):
            return []
        meas = {'accuracy': 0.5, 'relevance': 0.5}
        trace = self.request.trace + [TraceItem('QuestionParsing-Grammatical', tree, meas)]
        response = Response('en', tree, meas, trace)
        return [response]
