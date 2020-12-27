import os, shutil # folder management
import csv # used to read and write .csv files
from termcolor import cprint # used to customize terminal output and facilitate understanding


# Relative Path
filePath = os.path.dirname(os.path.realpath(__file__))

# triple get in the file
file = open(str(filePath)+'/Triple/pattern_triples.csv', 'r', newline='')
reader = csv.reader(file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)

# triple save file
file1 = open(str(filePath)+'/Triple/pattern_triples.csv', 'a', newline='')
writer = csv.writer(file1 ,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# code generated to create new triples when we have the multiple subject
newTriple = []
numberNerTriple = 0
for row in reader:
    if row[0].find("and") == 6:
        subjects = row[0].split("and") # list of subjects
        for sub in subjects: # for each subject on the list I generate a new triple
            numberNerTriple += 1
            sub = sub.replace(" ","")
            newTriple.append(sub)
            newTriple.append(row[1])
            newTriple.append(row[2])
            writer.writerow(newTriple) # add each new triple to the triple file
            print(newTriple)
            newTriple = []
   

cprint("\nIl numero di triple aggiunte è:"+str(numberNerTriple),"blue", attrs=['bold'])

exit()


