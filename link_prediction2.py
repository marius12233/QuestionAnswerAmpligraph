import spacy
import json
from tqdm import tqdm
import pandas as pd
import numpy as np
import ampligraph
from ampligraph.evaluation import evaluate_performance
from ampligraph.latent_features import save_model, restore_model
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
import numpy as np
import copy
from sent2vec.vectorizer import Vectorizer
import difflib

def most_similar_sentences(query, sentences):
    return difflib.get_close_matches(query, sentences)


def load_question_from_json(path="Question\\question.json"): 
    with open(path, "r") as fp:
        question=json.load(fp)
    question=json.loads(question)
    subj, rel, obj = None, None, None
    triple = [subj, rel, obj]
    objs = ("subject", "predicate", "object")

    #TO DO: case in which question is a list
    for i, obj in enumerate(objs):
        if question[obj]["type"]=="resource":
            triple[i] = question[obj]["value"] 
        elif question[obj]["type"]=="list":
            x=[]
            for object_ in question[obj]["list"]:
                x.append(object_["value"])
            triple[i] = x
        elif question[obj]["type"]=="missing":
            triple[i]="?"
    return triple

def build_missing_links(subjects, relations, objects, num_rel=5,n=1):
    """
    This function builds the query triples 
    """
    triples = load_question_from_json()
    sentences = [subjects, relations, objects]
    new_sentences = [[],[],[]]
    for i,element in enumerate(triples):
        #Se l'elemento è una lista mi prendo l'elemento della lista con il maggiore score 
        if isinstance(element,list):
            element = element[0:num_rel]
            for el in element:
                matching = difflib.get_close_matches(el, sentences[i],n=n)
                print(el)
                print(matching)
                new_sentences[i]+=matching
        
        elif isinstance(element,str):
            if element=="?":
                new_sentences[i]+=[element]
            else:
                matching = difflib.get_close_matches(element, sentences[i],n=n)
                new_sentences[i]+=matching

    max_len = max([len(ref) for ref in new_sentences])

    print(new_sentences)
    for ref in new_sentences:
        print(ref)
        if len(ref)<max_len:
            ref+=([ref[-1]]*(max_len-len(ref)))

    return new_sentences


def load_dataset(path):
    df=pd.read_csv(path)
    subjects=df["subj"].values.tolist()
    relations=df["rel"].values.tolist()
    objects=df["obj"].values.tolist()
    return subjects, relations, objects

def build_object_missing_triples(subj, rel, objects_dataset):
    triples = []
    for obj in objects_dataset:
        triples.append([subj, rel, obj])
    return triples

def build_subject_missing_triples(obj, rel, subjects_dataset):
    triples = []
    for subj in subjects_dataset:
        triples.append([subj, rel, obj])
    return triples

def link_prediction(subj, rel, obj, subjects, relations, objects):
    model = restore_model('./best_model.pkl')
    #triple = [subj, rel, obj]
    triples=[]

    for s,r,o in zip(subj, rel, obj):

        if s=="?":
            triples+=build_subject_missing_triples(o, r, subjects)
        elif o=="?":
            triples+=build_object_missing_triples(s, r, objects)
    
    #print(triples.shape)
    triples=np.array(triples)
    ranks_unseen = evaluate_performance(
        triples, 
        model=model, 
        corrupt_side = 's+o',
        use_default_protocol=False, # corrupt subj and obj separately while evaluating
        verbose=True
    )
    idx=np.argmin(ranks_unseen)
    response = None
    if subj=="?":
        response = triples[idx]
    else:
        response = triples[idx]
    return response
    

if __name__=="__main__":
    #sentence_similarity("lost", "misplace")
    #triple=build_links(["Dante","Virgil", "Dante and Virgil"], ["lost","lost in"], ["obj1","obj2"])

    subjects, relations, objects = load_dataset("Triple/complete_triples.csv")
    triple=build_missing_links(subjects, relations, objects)
    subj, rel, obj = triple[0], triple[1], triple[2]
    print("Triple: \n")
    print(subj, rel, obj)
    response=link_prediction(subj, rel, obj, subjects, relations, objects)
    print(response)
   
    """
    subjects, relations, objects = load_dataset("Triple/dep_triples.csv")
    triple=build_missing_links(subjects, relations, objects)
    print(triple)
    
    print("ranked" in relations)
    query="ranked"
    print(difflib.get_close_matches(query, relations,n=5))
    """
    #w,s=search_in_sentencies("ranked", relations, threshold=0.3)
    #print(w)



    