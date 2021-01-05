import os
import sys
from link_prediction import *

def query(question):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir('ppp\\demo\\')
    Q="_".join(question.split(" "))
    cmd=("{0} demo6.py --question "+Q).format(
                sys.executable
            )
    os.system(cmd)
    os.chdir(dir_path)

def _merge_csv():
    cmd=("{0} utils.py").format(
                sys.executable)
    os.system(cmd)  

def load_and_extract_Canti(start, end):
    #os.chdir('C:\\Users\\mario\\tsproject\\')
    cmd=("{0} InformationExtractingNltk.py --start {1} --stop {2}").format(
                sys.executable, start, end
            )
    os.system(cmd) 
    _merge_csv()

def train_model():
    cmd=("{0} ampligraph_train.py").format(
                sys.executable
            )
    os.system(cmd) 


def predict_link(model):
    subjects, relations, objects = load_dataset("Triple/complete_triples.csv")
    triple=build_missing_links(subjects, relations, objects)
    subj, rel, obj = triple[0], triple[1], triple[2]
    print("Triple: \n")
    print(subj, rel, obj)
    response=link_prediction(model,subj, rel, obj, subjects, relations, objects)
    print("Response: ", response)
    if subj[0]=="?":
        return response[0]
    else:
        return response[2]   

def load_and_extract_File():
    cmd=("{0} ExtractingInformationNltk_FromFILE.py").format(
                sys.executable
            )
    os.system(cmd) 
    _merge_csv()

if __name__=="__main__":
    #load_and_extract_Canti(3, 4)
    #train_model()
    #query(question)
    load_and_extract_File()
