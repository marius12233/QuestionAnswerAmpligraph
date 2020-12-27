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

def sentence_similarity2(vec1, vec2):
    dist = spatial.distance.cosine(vec1, vec2)
    #dist = np.linalg.norm(vec1 - vec2)
    #dist = 100 - dist
    return 1-dist

def sentence_similarity3(text1, text2):
    #nlp = spacy.load('en')
    nlp = spacy.load("en_core_web_md")
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity

def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]

def search_in_sentencies2(sentence, sentencies, threshold=0.3):
    """
    Find correspondences between relation and one of relations and return relations which 
    overcome the threshold
    """
    #Iterate through relations
    max_similarity=0
    most_similar_sentence=""

    new_sentencies = copy.deepcopy(sentencies)
    new_sentencies.insert(0,sentence)
    vectorizer = Vectorizer()
    vectorizer.bert(new_sentencies)
    vectors_sentences = vectorizer.vectors
    
    for i,sent in enumerate(tqdm(vectors_sentences[1:])):
        #print("SIMILARITY BETWEEN: \n", sent, sentencies)
        similarity = sentence_similarity2(sent,vectors_sentences[0])   #compute similarity score
        print(sentencies[i], " : ", similarity)
        if similarity > max_similarity:
            max_similarity=similarity
            most_similar_sentence=new_sentencies[i+1]

    #if max_similarity < threshold:
    #    raise Exception("There are not correspondencies...")
    return most_similar_sentence, max_similarity


def search_in_sentencies(sentence, sentencies, threshold=0.3):
    """
    Find correspondences between relation and one of relations and return relations which 
    overcome the threshold
    """
    #Iterate through relations
    max_similarity=0
    most_similar_sentence=""
    similar_sentencies=[]

    for i,sent in enumerate(tqdm(sentencies)):
        #print("SIMILARITY BETWEEN: \n", sent, sentencies)
        similarity = sentence_similarity(sent,sentence)   #compute similarity score
        if similarity > max_similarity:
            max_similarity=similarity
            most_similar_sentence=sent
            similar_sentencies.append(sent)
    print(similar_sentencies)
    #if max_similarity < threshold:
    #    raise Exception("There are not correspondencies...")
    return most_similar_sentence, max_similarity

def load_question_from_json(path="Question/question.json"):
    with open(path, "r") as fp:
        question=json.load(fp)
    question=json.loads(question)
    subj, rel, obj = None, None, None
    triple = [subj, rel, obj]
    objs = ("subject", "predicate", "object")

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

def build_links(subjects, relations, objects, num_rel=5):
    triple = load_question_from_json()
    new_triples = [0,0,0]
    d = {0:subjects, 1:relations, 2:objects}
    for i,element in enumerate(triple):
        #Se l'elemento è una lista mi prendo l'elemento della lista con il maggiore score 
        if isinstance(element,list):
            element = element[0:num_rel]
            print(element)
            max_score=0
            new_sentence=""
            for el in element:
                try:
                    print(el)
                    sentence,score = search_in_sentencies2(el, d[i], threshold=0.3)
                    print(sentence, score)
                    if score > max_score:
                        max_score=score
                        new_sentence=sentence

                except Exception as e:
                    print(e)
                    continue

            new_triples[i]=new_sentence
        
        elif isinstance(element,str):
            if element=="?":
                new_triples[i]=element
            else:
                try:
                    sentence,score = search_in_sentencies2(element, d[i], threshold=0.3)
                except:
                    continue

                new_triples[i]=sentence

    return new_triples


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
    return np.array(triples)

def build_subject_missing_triples(obj, rel, subjects_dataset):
    triples = []
    for subj in subjects_dataset:
        triples.append([subj, rel, obj])
    return np.array(triples)

def link_prediction(subj, rel, obj, subjects, relations, objects):
    model = restore_model('./best_model.pkl')
    list_to_iterate=None
    triple = [subj, rel, obj]
    triples=[]
    if subj=="?":
        triples=build_subject_missing_triples(obj, rel, subjects)
    else:
        triples=build_object_missing_triples(subj, rel, objects)
    #print(triples)
    #print(triples.shape)
    ranks_unseen = evaluate_performance(
        triples, 
        model=model, 
        corrupt_side = 's+o',
        use_default_protocol=False, # corrupt subj and obj separately while evaluating
        verbose=True
    )
    print(ranks_unseen)
    idx=np.argmin(ranks_unseen)
    response = None
    if subj=="?":
        response = subjects[idx]
    else:
        response = objects[idx]
    return response
    

if __name__=="__main__":
    #sentence_similarity("lost", "misplace")
    #triple=build_links(["Dante","Virgil", "Dante and Virgil"], ["lost","lost in"], ["obj1","obj2"])

    """
    subjects, relations, objects = load_dataset("Triple/dep_triples.csv")
    triple=build_links(subjects, relations, objects)
    subj, rel, obj = triple[0], triple[1], triple[2]
    print("Triple: \n")
    print(subj, rel, obj)
    response=link_prediction(subj, rel, obj, subjects, relations, objects)
    print(response)
    """
 
    subjects, relations, objects = load_dataset("Triple/complete_triples.csv")
    print("ranked" in relations)
    query="ranked"
    print(difflib.get_close_matches(query, relations,n=5))
    #w,s=search_in_sentencies("ranked", relations, threshold=0.3)
    #print(w)



    