import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()

def print_dot(relations,line):
    obj_set = set([])
    print("digraph relations {")
    for r in relations:
        #if r[0] != "det":
        obj_set.add(r[1])
        obj_set.add(r[2])
    for i in obj_set:
        print("\t\"{0}\"[label=\"{0}\",shape=box];".format(i))
    for r in relations:
        #if r[0] != "det":
        print("\t\"{0}\" -> \"{1}\"[label=\"{2}\"];".format(r[1],r[2],r[0]))
    print("\tlabelloc=\"t\"");
    print("\tlabel=\"%s\";" % line)
    print("}")

if __name__ == "__main__":
    line=input("")
    result = nlp.parse(line)
    print_dot(result['sentences'][0]['indexeddependencies'],line)
