import pandas as pd
import numpy as np
import time
import re
import json

#Spacy
#import spacy
#nlp = spacy.load('en_core_web_sm')
#NLTK
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from . import CleanData as clean
nltk.download('brown')
nltk.download('punkt')

class AspectsAnalysis():
    def get_nouns_tag(newText, aspect_list):
        tagged = nltk.pos_tag(newText)
        for (word, tag) in tagged:
            if tag in ['NN']:  # If the word is a proper noun
                aspect_list.append(word)

    # remove all pronouns
    def get_nouns_pos(text):
        for t in text:
            if (t.pos_ == "NOUN"):
                return text

        return ""

    def get_nouns_setiment(nouns_list,data):
        tex = []
        pos_count = []
        neg_count = []
        for i in nouns_list:
            pos = 0
            neg = 0
            for j in range(len(data)):
                if i in data.loc[j]['review']:
                    if data.loc[j]['sentiment'] == 'positive':
                      pos += 1
                    if data.loc[j]['sentiment'] == 'negative':
                      neg += 1

        tex.append(i)
        pos_count.append(pos)
        neg_count.append(neg)
        return tex,pos_count,neg_count

    def get_aspects(self , data):
        # text = [cleanhtml(t) for t in data['review']]
        tf_idf = Counter(" ".join(data['review']).split()).most_common(800)
        dic = dict(tf_idf)
        llist = []
        self.get_nouns_tag(dic.keys(), llist)
        # llist = [nlp(llist[t]) for t in range(len(llist))]
        # aspect_list = [get_nouns_pos(t) for t in llist ]
        # aspect_list = [str(aspect_list[t][0]) for t in range(len(aspect_list)) if aspect_list[t] != [] and aspect_list[t] !="" ]
        new_dic = {}
        for i in range(len(llist)):
            new_dic[llist[i]] = dic.get(llist[i])
        noun,pos,neg = self.get_nouns_setiment(list(new_dic.keys())[:6],data)
        # newData = pd.DataFrame({'word':noun,'pos':pos,'neg':neg})
        return noun,pos,neg


