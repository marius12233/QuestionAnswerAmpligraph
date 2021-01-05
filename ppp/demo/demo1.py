#from corenlp import StanfordCoreNLP
from nltk.parse import CoreNLPParser

corenlp_dir = "C:\\Users\\mario\\stanfordnlp_resources\\stanford-corenlp-full-2018-10-05\\"
corenlp =  CoreNLPParser(url='http://localhost:9000')  # wait a few minutes...

result = corenlp.raw_parse("What is birth date of the wife of the first black president of the United States?")

#print(result['sentences'][0]['dependencies'])
print(result)