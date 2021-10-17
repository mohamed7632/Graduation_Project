import pandas as pd
import numpy as np
import time
import re
import en_core_web_sm
#Spacy
import spacy as s
nlp = en_core_web_sm.load()
nlp = s.load('en_core_web_sm')
#NLTK
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
#from wordcloud import WordCloud, STOPWORDS
#from wordcloud import WordCloud, STOPWORDS

class Analysis():
    def hashtag_analysis(all_reviews):
        tweets = all_reviews[all_reviews['platform'] == 'twitter']
        hashtags = []
        for tweet in tweets['review']:
            ht = re.findall(r"#(\w+)", tweet)
            hashtags.append(ht)

        hashs = sum(hashtags, [])
        hashs[:10]

        freq = nltk.FreqDist(hashs)
        d = pd.DataFrame({'Hashtag': list(freq.keys()),
                          'Count': list(freq.values())})

        d = d.nlargest(columns='Count', n=10)
        # js = d.to_json(orient='records')
        labels = d.Hashtag.tolist()
        counts = d.Count.tolist()

        return labels, counts

    def location_analysis(all_reviews):
        states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                  'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                  'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                  'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New York', 'New Mexico',
                  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                  'West Virginia', 'Wisconsin', 'Wyoming']

        stateCodes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                      'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                      'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                      'WI', 'WY']

        stateMapping = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
                        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
                        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
                        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts',
                        'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
                        'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NY': 'New York',
                        'NM': 'New Mexico', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
                        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
                        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
                        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin',
                        'WY': 'Wyoming'}

        tweets = all_reviews[all_reviews['platform'] == 'twitter']
        tweet_location_df = tweets
        for index, row in tweets.iterrows():
            flag = 0
            if row.location:
                locationSplit = row.location.split(',')
                for word in locationSplit:
                    # Strip remove spaces
                    word_stripped = word.strip()
                    if word_stripped in states:
                        flag = 1
                        row['state'] = word_stripped
                    elif word_stripped in stateCodes:
                        flag = 1
                        row['state'] = stateMapping[word_stripped]
            if flag == 0:
                tweet_location_df = tweet_location_df.drop(index=index)
            else:
                tweet_location_df.loc[index, 'state'] = row['state']

        freq = nltk.FreqDist(tweet_location_df['state'])
        d = pd.DataFrame({'State': list(freq.keys()),
                          'Count': list(freq.values())})
        
        # js = d.to_json(orient='records')
        labels = d.State.tolist()
        counts = d.Count.tolist()
        return labels , counts

    # def wordcloud(df):

        # #Word Cloud
        # words = ''
        # # stopwords = set(STOPWORDS)

        # words = ' '.join([review for review in df['review']])

        # counts = WordCloud().process_text(words)

        # k = Counter(counts)
        
        # # Finding 3 highest values
        # high = k.most_common(300) 
        
        # labels_wordcloud = []
        # counts_wordlcoud = []
        
        # for i in high:
        #     labels_wordcloud.append(i[0])
        #     counts_wordlcoud.append(i[1])

        # return labels_wordcloud, counts_wordlcoud
        high = df['review'].most_common(500)

        return []
    def line_analysis(all_reviews):
        reviews = all_reviews[all_reviews['platform'] == 'amazon']
        # print(reviews)
        reviews['date'] = pd.to_datetime(reviews['date'])
        print(1)
        dt2021 = reviews[reviews['date'].dt.year == 2021]
        dt2021['month'] = pd.DatetimeIndex(dt2021['date']).month
        print(2)
        dt2021_positive = dt2021[dt2021['sentiment'] == 'positive']
        dt2021_negative = dt2021[dt2021['sentiment'] == 'negative']
        #Get Labels and Counts for positive reviews
        dt2021_positive = dt2021_positive[['month', 'sentiment']]
        values_positive = dt2021_positive.month.value_counts().sort_index()
        labels_positive = list(values_positive.keys())
        counts_positive = list(values_positive)

        print(labels_positive)
        print(counts_positive)
        # Get Labels and Counts for negative reviews
        dt2021_negative = dt2021_negative[['month', 'sentiment']]
        values_negative = dt2021_negative.month.value_counts().sort_index()
        labels_negative = list(values_negative.keys())
        counts_negative = list(values_negative)

        print(labels_negative)
        print(counts_negative)
        return labels_positive, counts_positive, labels_negative, counts_negative    