#!/usr/bin/env python3

############ IMPORT LIBRARY ############
import nltk # used to perform Natural Language Processing
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.draw import TreeView # viewing and creating tree folder
from nltk.tag.util import untag # tree to triple
import os, shutil # folder management
from termcolor import cprint # used to customize terminal output and facilitate understanding
import csv # used to read and write .csv files
import ExtractTextFromWeb #script to retrieve text from a url
import subprocess, sys # used to subprocess to add triples
<<<<<<< HEAD
from soie import text2csvtriples
=======

>>>>>>> 0c0540049da83f8841ca4ba8a2300bcbdf10859b

# Relative Path
filePath = os.path.dirname(os.path.realpath(__file__))

############ FOLDER AND FILE SETUP  ############
# creation of folders to save knowledge graphs in tree format
if os.path.exists(str(filePath)+'/Sentences') == False:
    os.mkdir(str(filePath)+'/Sentences')
else: 
    shutil.rmtree(str(filePath)+'/Sentences')
    os.mkdir(str(filePath)+'/Sentences')
    
# creation of folders for triple saving found in file.csv
if os.path.exists(str(filePath)+'/Triple') == False:
    os.mkdir(str(filePath)+'/Triple')
else:
    shutil.rmtree(str(filePath)+'/Triple') 
    os.mkdir(str(filePath)+'/Triple')

# creation of folders to save named enity recognition in tree format
if os.path.exists(str(filePath)+'/NamedEntity') == False:
    os.mkdir(str(filePath)+'/NamedEntity')
else: 
    shutil.rmtree(str(filePath)+'/NamedEntity')
    os.mkdir(str(filePath)+'/NamedEntity')

# triple save file
<<<<<<< HEAD
file = open(str(filePath)+'/Triple/pattern_triples.csv', 'w', newline='')
=======
file = open(str(filePath)+'/Triple/triple.csv', 'w', newline='')
>>>>>>> 0c0540049da83f8841ca4ba8a2300bcbdf10859b
writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

############ ENVIRONMENT SETUP  ############
# nltk.download('punkt')
# nltk.download('all')


############ PHASE LOADING TEXT FROM FILE ############

import glob, os
number_files=0
text = ""
os.chdir("Text/")
for file_read in glob.glob("*.txt"):
    number_files += 1
    text += open(file_read, "r").read() +".\n"
<<<<<<< HEAD
os.chdir("../")
text2csvtriples(text)
cprint("\n\n############ INPUT TEXT ############","green", attrs=['bold'])
cprint("\nNumero di file letti: "+str(number_files),"blue", attrs=['bold'])

=======

cprint("\n\n############ INPUT TEXT ############","green", attrs=['bold'])
cprint("\nNumero di file letti: "+str(number_files),"blue", attrs=['bold'])

print(text)
>>>>>>> 0c0540049da83f8841ca4ba8a2300bcbdf10859b


cprint("\n############ PHASE CHINKING ############","green", attrs=['bold'])
word_tokenizer_output = word_tokenize(text)

# words to delete
stopWords = ["between","an","again","below","than","when","before"
,"each","from","then","here","by","what","because","why","but","back"
,"only","as","of"]
print("Words to delete: \n"+str(stopWords))

wordsFiltered = []
for w in word_tokenizer_output:
    if w not in stopWords:
        wordsFiltered.append(w)


cprint("\n############ FILTERED TEXT ############","green", attrs=['bold'])
text = ""
for ele in wordsFiltered:
    text += ele+str(" ") 
print(text)



cprint("\n\n############ PHASE SENTENCES TOKENIZING (text --> sentences) ############\n","green", attrs=['bold'])
# I load the PUNKT model for the division into sentences
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle') 
sentences_tokenizer_output = sent_detector.tokenize(text)
print('\n-------------------------\n'.join(sentences_tokenizer_output))



cprint("\n\n############ PHASE WORDS TOKENIZING (sentence --> words) ############\n","green", attrs=['bold'])
word_tokenizer_output = word_tokenize(text)
print(' --- '.join(word_tokenizer_output))



cprint("\n\n############ PHASE CATEGORIZING AND POS-TAGGING WORDS ############\n","green", attrs=['bold'])
tagged_word = nltk.pos_tag(word_tokenizer_output)
print(tagged_word)


cprint("\n\n############ PHASE PATTERN SELECTION ############","green", attrs=['bold'])
pattern = r"""
NP: {<DT>? <PRP.>? <JJ>* <NN.*> <CC> <DT>? <JJ>* <NN.*> | <DT>? <PRP.>? <JJ>* <NN.*>+ }
VB: { <TO>? <MD>? <VB.?> <VB.?>? <TO>? <VB.?> <TO>? | <TO>? <MD>? <VB.?>* <TO>? }
CHUNK2: {<PRP> <VB> <NP>}
CHUNK1: {<NP> <VB> <NP>}
""" 
print(pattern)



cprint("\n############ PHASE CHUNKING AND TRIPLE DETECTION ############","green", attrs=['bold'])
i=1
chunk1=0
chunk2=0

############ CODE MAIN ############
for sts in sentences_tokenizer_output:
    cprint("\nSentence in analysis: ","blue", attrs=['bold'])
    print(sts)
    word_tagged_sts = nltk.pos_tag(word_tokenize(sts))
    cprint("\nPOS-Tagging sentence:","blue", attrs=['bold'])
    print(word_tagged_sts)
 
    # pattern application
    chunkParser_sts = nltk.RegexpParser(pattern, loop=1)
    chunked_sts = chunkParser_sts.parse(word_tagged_sts)
    cprint("\nSentence division into chunk:","blue", attrs=['bold'])
    print(chunked_sts)

    # named entity recognition and saving graph
    namedEnt = nltk.ne_chunk(word_tagged_sts, binary=False)
    TreeView(namedEnt)._cframe.print_to_file(str(filePath)+'/NamedEntity/'+str(i)+'_namedEntity.ps')
    chunk1=0
    chunk2=0

    # saving graph of the knowledge of the unprocessed sentence
    TreeView(chunked_sts)._cframe.print_to_file(str(filePath)+'/Sentences/'+str(i)+'_sentence.ps')
   
    # count of patters found
    for subtree in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK1'):
        chunk1 +=1 
    # print('chunk1: '+str(chunk1))
    for subtree1 in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK2'):
        chunk2 +=1 
    # print('chunk2: '+str(chunk2))

    if chunk1 + chunk2 != 4:
        flag=True
    else:
        flag=False

    # substitution of subject identified in chunk1 with pronoun identified in chunk2
    for subtree in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK1'):
        sog = subtree[0] 
        # print('1: '+str(sog))
        
        for subtree1 in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK2'):
            subtree1[0] = sog
            # print('2: '+str(subtree1[0]))
            if chunk1 == chunk2:
                subtree1.set_label("CHUNK")
                chunk2 -= 1
            else:
                if flag == True:
                    subtree1.set_label("CHUNK")
                else:
                    chunk1 -=1
                    
    # To normalize all labels with "CHUNK"
    for subtree in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK1'):
        subtree.set_label("CHUNK")

    # saving graph of the knowledge of the processed sentence
    TreeView(chunked_sts)._cframe.print_to_file(str(filePath)+'/Sentences/'+str(i)+'_sentenceProccessed.ps')

    cprint("\nPHASE CHUNK TO TRIPLE CONVERSION\nTriple identified:","blue", attrs=['bold'])
    # saving graph of the knowledge of the processed sentence
    chunk = []
    for subtree in chunked_sts.subtrees(filter=lambda t: t.label() == 'CHUNK'):
        for listOfChunck in subtree:
            listOfChunck = untag(listOfChunck)
            # print(listOfChunck)
            listToStringChunck = ' '.join([str(elem) for elem in listOfChunck])
            chunk.append(listToStringChunck)
            # print(listToStringChunck)
        
        print(chunk)                 
      
        writer.writerow(chunk)
        chunk = [] 

    cprint("\n-----------------------------------------------------------------------","yellow", attrs=['bold'])
    i +=1

# closing file used for saving triples
file.close()

## triple addition phase to extend dataset when we have multiple subjects
cprint("\n############ PHASE ADDITION TRIPLE ############\n\n","green", attrs=['bold'])
<<<<<<< HEAD
#subprocess.Popen('ulimit -v unlimited', shell=True)
subprocess.Popen([sys.executable, "TripleExtension.py"]) 
=======
subprocess.Popen('ulimit -v unlimited', shell=True)
subprocess.Popen([sys.executable, "/home/mivia/ProgettoTS/TripleExtension.py"]) 
>>>>>>> 0c0540049da83f8841ca4ba8a2300bcbdf10859b
