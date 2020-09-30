'''
    Author : Shubham Agrawal
    Roll no: 2019201085
    Institute: IIIT-Hyderabad
'''

import xml.sax
import re
import string
import timeit
import os
from os import listdir
from os.path import isfile, join
import sys

title_file_name = "title_mapping.txt"
title_file = open(title_file_name, 'a+')
index_file = 0
counter = 0

# Text Processing
def remove_punctuation(line):
    return line.translate(str.maketrans('','',string.punctuation))

#for stemming the data
from nltk.tokenize import word_tokenize
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


stemmed_words={}
Inverted_Index = {}

def add_to_invereted_index(word, doc_id, type_):
  global Inverted_Index, stemmed_words, stop_words, stemmer
  if word in stop_words:
    return
  if(len(word)<=3 and word.isdigit()):
    return

  if word in stemmed_words:
    word = stemmed_words[word]
  else:
    stemmed_words[word] = stemmer.stem(word)
    word = stemmed_words[word]

  if word in Inverted_Index:
    if doc_id in Inverted_Index[word]:
      if type_ in Inverted_Index[word][doc_id]:
        Inverted_Index[word][doc_id][type_]+=1
      else:
        Inverted_Index[word][doc_id][type_] = 1
    else:
      Inverted_Index[word][doc_id] = {type_ : 1}
  else:
    Inverted_Index[word] = {doc_id : {type_ : 1}}


def write_index():
  global index_file, Inverted_Index
  index_file+=1
  ff2 = "index/inverted_index_"+str(index_file)
  f = open(ff2, 'w')
  for word in sorted(Inverted_Index):
    data=str(word)+" "
    for doc_id in Inverted_Index[word]:
      ll = [0, 0, 0, 0, 0, 0] #[t, b, c, i, r, e]
      for type_ in Inverted_Index[word][doc_id]:
        if(type_ == 't'):
          ll[0] = Inverted_Index[word][doc_id][type_]
        if(type_ == 'b'):
          ll[1] = Inverted_Index[word][doc_id][type_]
        if(type_ == 'c'):
          ll[2] = Inverted_Index[word][doc_id][type_]
        if(type_ == 'i'):
          ll[3] = Inverted_Index[word][doc_id][type_]
        if(type_ == 'r'):
          ll[4] = Inverted_Index[word][doc_id][type_]
        if(type_ == 'e'):
          ll[5] = Inverted_Index[word][doc_id][type_]

      data += str(doc_id)
      if(ll[0]!=0):
        data += "|"+"t"+str(ll[0])
      if(ll[1]!=0):
        data += "|"+"b"+str(ll[1])
      if(ll[2]!=0):
        data += "|"+"c"+str(ll[2])
      if(ll[3]!=0):
        data += "|"+"i"+str(ll[3])
      if(ll[4]!=0):
        data += "|"+"r"+str(ll[4])
      if(ll[5]!=0):
        data += "|"+"e"+str(ll[5])

      data +=" "
    data += '\n'
    f.write(data)
  f.close() 

  

#Processing text
def toCamelCase(line):
  return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', line)
tokens_count=0

def process_title(doc_id, title):
  global tokens_count
  words = toCamelCase(str(title))
  tokens_count+=1
  for word in words:
    add_to_invereted_index(word.lower(), doc_id, "t")

def process_text1(doc_id, text):
  global tokens_count
  junk = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)
  text = junk.sub(' ',text)
  # text = remove_punctuation(text)
  words = re.split(r'[^A-Za-z0-9]+', text)
  tokens_count += len(words)
  # words = text.split()
  for word in words:
    if(len(word)>1):
      add_to_invereted_index(word, doc_id, "b")

def process_text(doc_id, text):
  global tokens_count
  global title_file
  tokens = []
  links = []
  info_box = []
  body = []
  categories = []
  references = []

  #Convert to lower text
  text = text.lower()
  css = re.compile(r'{\|(.*?)\|}',re.DOTALL)
  cite = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)
  files = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
  urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
  # junk = re.compile(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",re.DOTALL)

  # Categories
  catRegExp = r'\[\[category:(.*?)\]\]'
  categories = re.findall(catRegExp,text,flags=re.MULTILINE)
  categories = ' '.join(categories)
  #categories = junk.sub(' ',categories)
  # categories = categories.split()
  tokenList = re.split(r'[^A-Za-z0-9]+', categories)

  for word in categories:
    if(len(word)>1):
      add_to_invereted_index(word, doc_id, "c")


  # Infobox
  infoRegExp = r'{{infobox(.*?)}}'
  info_box = re.findall(infoRegExp,text,re.DOTALL)
  for infoList in info_box:
    tokenList = []
    tokenList = re.findall(r'=(.*?)\|',infoList,re.DOTALL)
    tokenList = ' '.join(tokenList)
    #tokenList = junk.sub(' ',tokenList)
    # tokenList = tokenList.split()
    tokenList = re.split(r'[^A-Za-z0-9]+', tokenList)
    
    for word in tokenList:
      if(len(word)>1):
        add_to_invereted_index(word, doc_id, "i")

  # References
  refRegExp = r'== ?references ?==(.*?)=='
  references = re.findall(refRegExp,text,flags=re.DOTALL)

  references = ' '.join(references)
  # print(references)
  #references = junk.sub(' ',references)
  # references = references.split()
  words = re.split(r'[^A-Za-z0-9]+', references)

  for word in references:
    if(len(word)>1):
      add_to_invereted_index(word, doc_id, "r")
      
  # External Links
  ei=0
  ci=len(text)
  try:
    ei = text.index('=external links=')+20
    ci = text.index('[[category:')+20
  except:
    pass

  links = text[ei:ci]
  links = re.findall(r'\[(.*?)\]',text,flags=re.MULTILINE)

  links = ' '.join(links)
  # print(references)
  #links = junk.sub(' ',links)
  # links = links.split()
  words = re.split(r'[^A-Za-z0-9]+', links)

  for word in links:
    if(len(word)>1):
      add_to_invereted_index(word, doc_id, "e")


  text = urls.sub('',text)
  text = cite.sub('',text)
  text = files.sub('',text)
  text = css.sub('',text)
  # text = junk.sub(' ',text)
  # text = remove_punctuation(text)
  words = re.split(r'[^A-Za-z0-9]+', text)
  tokens_count += len(words)
  title_file.write(str(len(words))+"\n")
  # words = text.split() 
  for word in words:
    if(len(word)>1 and len(word) < 46):
      add_to_invereted_index(word, doc_id, "b")
    
    
# ContentHandler

class WikiContentHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.current_data_buffer = ""
        self.doc_id = 0
        self.text = ""
        self.has_title = False
        self.has_text = False
        self.title = ""
        self.text_size = 0
        self.flag=0


    def startElement(self, tag, attributes):
        global counter
        self.current_data_buffer = tag
        
        if (tag == "page"):
            #print("-- New Page --")
            counter+=1
            self.flag=1
            self.doc_id = counter
            
        elif (tag == "text"):
            self.text_size = attributes["bytes"]
            #print("TextSize: ", size)

    def endElement(self, tag):
        global title_file, Inverted_Index
        if (self.current_data_buffer == "title"):
            #print (self.doc_id,"Title: ",self.title)
            title_file.write(str(self.doc_id)+" "+self.title+" ")
            process_title(self.doc_id, self.title)
            self.title = ""
            
        elif (self.current_data_buffer == "text"):
            process_text(self.doc_id, self.text)
            # print ("Text: ", self.text)
            self.text = ""
        self.current_data_buffer=""

        if(self.doc_id%2000 == 0 and self.flag==1):
          print(self.doc_id, "Done")
          if(self.doc_id%10000 == 0):
            write_index()
            Inverted_Index.clear()
            Inverted_Index={}
            print("written ...", self.doc_id)

          self.flag=0
        
    
    def characters(self, content):
        if (self.current_data_buffer == "title"):
            self.title += content
            
        elif (self.current_data_buffer == "text"):
            self.text += content





print("Parsing Started")
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = WikiContentHandler()
parser.setContentHandler( Handler )
start_time = timeit.default_timer()
mypath = "../data"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# onlyfiles = sorted(onlyfiles)
# print(onlyfiles)
onlyfiles = ['xml_1', 'xml_2', 'xml_3', 'xml_4', 'xml_5',
              'xml_6', 'xml_7', 'xml_8', 'xml_9', 'xml_10']
              # 'xml_11', 'xml_12', 'xml_13', 'xml_14', 'xml_15',
              # 'xml_16', 'xml_17', 'xml_18', 'xml_19', 'xml_20',
              # 'xml_21', 'xml_22', 'xml_23', 'xml_24', 'xml_25',
              # 'xml_26', 'xml_27', 'xml_28', 'xml_29', 'xml_30',
              # 'xml_31', 'xml_32', 'xml_33', 'xml_34'
 # ]

for f in onlyfiles:
  parser.parse(join(mypath, f))
  print('Xml Done', f )



# parser.parse(filename)
stop_time = timeit.default_timer()
print("Parsing Completed")
print("Time Taken(seconds) : ", stop_time - start_time)

title_file.close()
print(counter)
write_index()
Inverted_Index.clear()
Inverted_Index={}
print("written ...")
print(index_file)



