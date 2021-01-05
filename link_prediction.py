import spacy
import json
from tqdm import tqdm
import pandas as pd
import numpy as np
import ampligraph
from ampligraph.evaluation import evaluate_performance
from ampligraph.latent_features import save_model, restore_model
from scipy import spatial
import numpy as np
import copy
from sent2vec.vectorizer import Vectorizer
import difflib
from bert_score import score
from bert_score import BERTScorer
import tensorflow as tf
import tensorflow_hub


def sentence_similarity2(vec1, vec2):
    dist = spatial.distance.cosine(vec1, vec2)
    #dist = np.linalg.norm(vec1 - vec2)
    #dist = 100 - dist
    return dist

def most_similar_sentences(query, sentences):
    return difflib.get_close_matches(query, sentences)

def load_question_from_json(path="Question/question.json"): 
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

def build_missing_links(subjects, relations, objects, num_rel=3,n=1):
    """
    This function builds the query triples 
    """
    
    ########### TF HUB ############
    # Decommentare il seguente codice se si vuole utilizzare la similarità semantica tra le parole

    #embed = tensorflow_hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")
    #input1 = tf.placeholder(tf.string)
    #input2 = tf.placeholder(tf.string)
    #encode1 = tf.nn.l2_normalize(embed(input1))
    #encode2 = tf.nn.l2_normalize(embed(input2))

    ########### TF HUB ############

    triples = load_question_from_json()

    print("Relations: ", triples[1])
    sentences = [subjects, relations, objects]
    new_sentences = [[],[],[]]
    for i,element in enumerate(triples):
        
        if isinstance(element,list):            
            #If we have the question e.g. "where is Dante?" we don't query 'is' but we use
            #words that reminds us to a location
            if "identity" in element:
                element.remove("identity")
                element.insert(0,"is a")

            if "location" in element:
                if "is" in element:
                    element.remove("is")
                if "been" in element:
                    element.remove("been")
                element.insert(0,"in")
            
            element = element[0:num_rel]
            element=element[::-1]
            for el in element:
                matching = difflib.get_close_matches(el, sentences[i],n=n, cutoff=0.6)
                print("Element list: ", el)

                #sen,_=search_in_sentencies2(el, sentences[i])

                """
                s1=[el]
                s2=sentences[i]
                sims=[]
                scores = tf.reduce_sum(tf.multiply(encode1, encode2), axis=1)
                with tf.Session() as session:
                    session.run(tf.global_variables_initializer())
                    session.run(tf.tables_initializer())

                    [similarity] = session.run([scores], feed_dict={
                        input1: [s for s in s1],
                        input2: [s for s in s2]
                    })
                    
                #sims = gse([el]*len(sentences[i]), sentences[i] )

                #print("tf hub sim: ", sims)
                print("Most similar: ", sentences[i][np.argmax(similarity)] )
                matching+=[sentences[i][np.argmax(similarity)]]
                """
                print(matching)
                
                new_sentences[i]+=matching
        
        elif isinstance(element,str): #Se la risorsa non è una lista
            if element=="?":
                new_sentences[i]+=[element]
            else:
                matching = difflib.get_close_matches(element, sentences[i],n=n, cutoff=0.6)
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

def link_prediction(model, subj, rel, obj, subjects, relations, objects):
    #model = restore_model('./best_model.pkl')
    #triple = [subj, rel, obj]
    triples=[]

    for s,r,o in zip(subj, rel, obj):

        if s=="?":
            triples+=build_subject_missing_triples(o, r, subjects)
        elif o=="?":
            triples+=build_object_missing_triples(s, r, objects)
    
    #print(triples.shape)
    triples=np.array(triples)
    print("All triples question: ", rel)
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
    model = restore_model('./best_model.pkl')
    subjects, relations, objects = load_dataset("Triple/complete_triples.csv")
    triple=build_missing_links(subjects, relations, objects)
    subj, rel, obj = triple[0], triple[1], triple[2]
    print("Triple: \n")
    print(subj, rel, obj)
    response=link_prediction(model, subj, rel, obj, subjects, relations, objects)
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



    