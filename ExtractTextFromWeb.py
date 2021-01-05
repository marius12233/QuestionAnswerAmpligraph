# Importa l'oggetto BeatifulSoup dal modulo bs4:
from bs4 import BeautifulSoup # BeautifulSoup is a Python library for extracting data from HTML files
from urllib.request import urlopen # used to access the selected link
import nltk # used to perform Natural Language Processing
import re # used to set a regular expression
from termcolor import cprint # used to customize terminal output and facilitate understanding

# function that allows you to extrapolate the text from the songs that the user wants to analyze
def selectText(start=None, stop=None):

    inputUser = True
    cprint("\nFrom which side do you want to start the analysis? (1 - 30): ","blue", attrs=['bold'])
    if not start:
        start = input("---> ")
    cprint("\nAt what song do you want to finish the analysis? (1 - 30): ","blue", attrs=['bold'])
    if not stop:
        stop = input("---> ")

    # check that the numbers of the songs selected by the user are correct
    while( inputUser ):
        a = re.match(r"^([1-2]{1})[0-9]?|^[0-9]{1}$|^(3){1}(0){1}", start)
        b = re.match(r"^([1-2]{1})[0-9]?|^[0-9]{1}$|^(3){1}(0){1}", stop)
        if a !=None and b != None:
            inputUser = False
        else:   
            inputUser = True 
            cprint("\nFrom which side do you want to start the analysis? (1 - 30): ","blue", attrs=['bold'])
            start = input("---> ")
            cprint("\nAt what song do you want to finish the analysis? (1 - 30): ","blue", attrs=['bold'])
            stop = input("---> ")      

    cprint("\nAnalysis of the canto(s):"+str(start)+"-"+str(stop),"yellow", attrs=['bold'])  
    stop = int(stop)-1
    start = int(start)-1
   
    url = "https://www.cliffsnotes.com/literature/d/the-divine-comedy-inferno/summary-and-analysis/canto-vii"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

  
    web = soup.findAll('a')   # I scroll through all the HTML tags that turn out to be links
    check = True
    flag = False
    b = ""
    arrayCantos = [] 

    if web:
        for elem in web:
            if elem.text == 'Canto I' and check:
                flag = True
                check = False

            if elem.text == 'Character Analysis':
                flag = False

            if flag:
                text = elem.text
                word = text.split()
                cantos = word[len(word)-1]
                cantos = cantos.replace("-","")
                arrayCantos.append(cantos.lower()) # I create the list that contains all the cantos
                

    testo = ""
    for i in range(start, stop):
        if len(arrayCantos[i]) > 6:
            print(arrayCantos[i])
            print(len(arrayCantos[i]))
            finalPath = 'cantos'
        else:
            finalPath = 'canto'


        url = 'https://www.cliffsnotes.com/literature/d/the-divine-comedy-inferno/summary-and-analysis/'+str(finalPath)+'-'+str(arrayCantos[i])
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        
        web = soup.findAll('p') # I scroll through all the HTML tags that appear to be paragraphs to get the text to be analyzed
        check = True
        flag = False
        if web:
            for a in web:
                if a.text == 'Summary' and check:
                    flag = True
                    check = False
                
                if a.text == 'Glossary':
                    flag = False
                
                if flag:
                    testo += a.text + " "
                    title = "----- Canto "+str(arrayCantos[i]).upper()+" -----."
                    testo = testo.replace("Summary", title)
                    testo = testo.replace("Analysis", "")
            
    return testo

        

            
        
        
