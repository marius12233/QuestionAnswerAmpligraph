from openie import StanfordOpenIE
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from spacy import displacy
import spacy
import nltk
import neuralcoref
import pandas as pd


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
    df.to_csv("Triple\\dep_triples.csv",index=False)
    return df



if __name__=="__main__":
    text="The economy of Victoria is highly diversified: service sectors including financial and property services, health, education, wholesale, retail, hospitality and manufacturing constitute the majority of employment. Victoria's total gross state product (GSP) is ranked second in Australia, although Victoria is ranked fourth in terms of GSP per capita because of its limited mining activity. Culturally, Melbourne is home to a number of museums, art galleries and theatres and is also described as the 'sporting capital of Australia'. The Melbourne Cricket Ground is the largest stadium in Australia, and the host of the 1956 Summer Olympics and the 2006 Commonwealth Games. The ground is also considered the spiritual home of Australian cricket and Australian rules football, and hosts the grand final of the Australian Football League (AFL) each year, usually drawing crowds of over 95,000 people. Victoria includes eight public universities, with the oldest, the University of Melbourne, having been founded in 1853."
    text2csvtriples(text)
"""
subjects=[]
pronoun_substitution = {}

for i,text in enumerate(texts.split(".")):
    subjects.append([])
    doc = nlp(text)
    entities=[]
    #displacy.serve(doc, style="dep")
    print("="*10)
    print(text)
    print("="*10)
    for w in doc.ents:
        #print(w.text, " ",w.label_)
        if w.label_=="PERSON" or w.label_=="NORP":
            entities.append(w.text)

    for j,tok in enumerate(doc):
        #print(tok.text, "...", tok.dep_, "...", tok.pos_,"...",tok.tag_,"...",nlp.vocab.morphology.tag_map[tok.tag_],"...")


        #elif (tok.tag_=="NNP" ) and (tok.dep_=="nsubj" or tok.dep_=="nsubjpass" or tok.dep_=="pobj") and not tok.tag_=="PRP":
        if tok.text in entities or ((tok.dep_=="nsubj" or tok.dep_=="nsubjpass" ) and (tok.pos_=="NOUN" or tok.pos_=="PROPN") ):
            print(tok.text, " candidate ", tok.tag_)
            is_already_in = False
            for s in subjects[i]:
                if tok.text==s.text:
                    is_already_in=True
            if not is_already_in:
                subjects[i].append(tok)

        elif tok.tag_=="PRP" or tok.pos_=="PROUN":
            
            j=i
            while len(subjects[j])==0:
                j-=1
            if not j==1:
                print(subjects[j-1])
            if not j==0:
                print(subjects[j])


            print(tok.text, " pron")
            for subj in subjects[::-1]:

                pass#if nlp.vocab.morphology.tag_map[tok.tag_]
    #print("\n ", subjects)
"""