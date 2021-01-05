from openie import StanfordOpenIE
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from spacy import displacy
import spacy
import nltk
import neuralcoref
import pandas as pd
import os


def text2csvtriples(text):
    nlp = spacy.load('en')
    neuralcoref.add_to_pipe(nlp)
    doc1 = nlp(text)
    text=doc1._.coref_resolved

    subjs=[]
    rels=[]
    objs=[]
    with StanfordOpenIE() as client:

        print('Text: %s.' % text)
        for triple in client.annotate(text):

            print('|-', triple)
            subjs.append(triple["subject"])
            rels.append(triple["relation"])
            objs.append(triple["object"])

    data = {"subj":subjs, "rel":rels, "obj":objs}
    df = pd.DataFrame(data, columns=["subj","rel","obj"])
    path = "Triple\\dep_triples.csv"
    if os.path.exists(path):
        df2 = pd.read_csv(path)
        df=pd.concat([df, df2], ignore_index=True, sort=False)
        
    df.to_csv(path,index=False)
    return df



if __name__=="__main__":
    text="The economy of Victoria is highly diversified: service sectors including financial and property services, health, education, wholesale, retail, hospitality and manufacturing constitute the majority of employment. Victoria's total gross state product (GSP) is ranked second in Australia, although Victoria is ranked fourth in terms of GSP per capita because of its limited mining activity. Culturally, Melbourne is home to a number of museums, art galleries and theatres and is also described as the 'sporting capital of Australia'. The Melbourne Cricket Ground is the largest stadium in Australia, and the host of the 1956 Summer Olympics and the 2006 Commonwealth Games. The ground is also considered the spiritual home of Australian cricket and Australian rules football, and hosts the grand final of the Australian Football League (AFL) each year, usually drawing crowds of over 95,000 people. Victoria includes eight public universities, with the oldest, the University of Melbourne, having been founded in 1853."
    text2csvtriples(text)
