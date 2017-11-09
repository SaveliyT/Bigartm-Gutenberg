
# coding: utf-8

# In[1]:


import artm
import zipfile
import os
import io
import nltk
import codecs

from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import brown


# In[2]:


nltk.download('stopwords')
stop_words= nltk.corpus.stopwords.words('english')
stop_word=""
for i in stop_words:
        stop_word =  stop_word+" "+i
print stop_word

ps = PorterStemmer()


# In[3]:


def unzip_folder(path):
    for filename in os.listdir(path):
        if (filename.endswith('.zip')):
            
            name = os.path.splitext(os.path.basename(filename))[0]
            if not os.path.isdir(name):
                try:
                    fzip = zipfile.ZipFile(path+'/'+filename)
                    fzip.extractall(path=path)
                except zipfile.BadZipfile, e:     
#                    print "BAD ZIP: "+filename
                    pass

            
        elif (os.path.isdir(path+'/'+filename)):
            unzip_folder(path+'/'+filename)


# In[4]:


def preprocess_folder(path):
    for filename in os.listdir(path):
        if (filename.endswith('.txt')):
            preprocess_file(path+'/'+filename) 
        elif (os.path.isdir(path + '/' + filename)):
            preprocess_folder(path+'/'+filename)


# In[5]:


def preprocess_file(filepath):
    flag = False
    text = io.open(filepath, 'r', encoding = 'ISO-8859-1')
    
    corp_list = []
    for line in text:
        if (line.startswith('*** END')):
            flag = False

        if (flag & len(line) != 0):
            for word in line.split(' '):
                try:
                    word = word.decode('utf-8')
                except UnicodeEncodeError:
                    continue
                word = word.lower()
                if ((word.isalpha()) & (word not in stop_word)):
                    corp_list.append(ps.stem(word))

        if (line.startswith('*** START')):
            flag = True


    string = ' '.join(corp_list)    
    
    
    vw_corpus = codecs.open(vw_file, 'a', 'utf-8')
    vw_corpus.write((' |text' + ' ' + string + '\n').encode('utf-8'))
    
    
    
    vw_corpus.close()
    text.close()


# In[6]:



vw_file = 'vw_gutenberg.txt'
corpus_file = 'gutenberg_corpus8.zip'
corpus_path = 'gutenberg_corpus8'

fzip = zipfile.ZipFile(os.curdir + '/' + corpus_file)

if (corpus_path not in os.listdir(os.curdir)) :
    os.mkdir(os.curdir + '/' + corpus_path)
fzip.extractall(path = (os.curdir + '/' + corpus_path))

print (corpus_file + ' extracted')

if(vw_file in os.listdir(os.curdir)):
    os.remove(os.curdir+'/'+vw_file)

unzip_folder(os.curdir + '/' + corpus_path)

print ('All files extracted')
preprocess_folder(os.curdir + '/' + corpus_path)

