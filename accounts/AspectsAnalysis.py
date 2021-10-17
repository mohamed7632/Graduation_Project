import pandas as pd
import numpy as np
import time
import re
import json

#Spacy
import spacy
nlp = spacy.load('en_core_web_sm')
#NLTK
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from . import CleanData as clean
nltk.download('stopwords')
nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
class AspectsAnalysis():
    def get_nouns_tag(self , newText, aspect_list):
        tagged = nltk.pos_tag(newText)
        for (word, tag) in tagged:
            if tag in ['NN']:  # If the word is a proper noun
                aspect_list.append(word)

    # remove all pronouns
    def get_nouns_pos(self,text):
        for t in text:
            if (t.pos_ == "NOUN"):
                return text

        return ""

    def get_nouns_setiment(self,nouns_list,data):
        tex = []
        pos_count = []
        neg_count = []
        for i in nouns_list:
            pos = 0
            neg = 0
            # print(len(data))
            # print(data['review'])
            for index, j in data.iterrows():
                #print(j['review'])
                if i in j['review']:
                    if j['sentiment'] == 'positive':
                      pos += 1
                    if j['sentiment'] == 'negative':
                      neg += 1

            tex.append(i)
            pos_count.append(pos)
            neg_count.append(neg)
        return tex,pos_count,neg_count

    def get_aspects(self , data):
        # stop = stopwords.words('english')
        new_data = data
        # new_data["review"] = new_data["review"].str.lower()
        # new_data["review"].apply(lambda x: [item for item in new_data["review"] if item not in stop])
        # print(new_data.loc[50:]['review'])
        # text = [cleanhtml(t) for t in data['review']]
        tf_idf = Counter(" ".join(data['review']).split()).most_common(500)
        dic = dict(tf_idf)
        # dic = dict((k.lower(), v) for k,v in dic.items())
        llist = []
        self.get_nouns_tag(dic.keys(), llist)
        llist = list(set(llist))
        llist = [nlp(llist[t]) for t in range(len(llist))]
        aspect_list = [self.get_nouns_pos(t) for t in llist ]
        aspect_list = [str(aspect_list[t][0]) for t in range(len(aspect_list)) if aspect_list[t] != [] and aspect_list[t] !="" ]
        # aspect_list = [t for t in aspect_list if not t.find('#')]
        # aspect_list = [t for t in aspect_list if not t.find('thing')]
        new_dic = {}
        for i in range(len(aspect_list)):
            new_dic[aspect_list[i]] = dic.get(aspect_list[i])
        noun,pos,neg = self.get_nouns_setiment(list(new_dic.keys())[:8],new_data)

        print(noun,pos,neg)
        # newData = pd.DataFrame({'word':noun,'pos':pos,'neg':neg})
        return noun,pos,neg

