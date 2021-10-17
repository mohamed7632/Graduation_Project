import pandas as pd
import numpy as np
import time
import re
from sklearn.feature_extraction.text import CountVectorizer
# from . import visionalyst_classifier_dt as x
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
# import joblib
# from joblib import dump
from joblib import load



class SentimentModel():
    def get_sentiment(df):
        print(len(df))
        # load the saved pipeline model
        pipeline = load('D:/grade four sec/G_project/Graduation/src/accounts/visionalyst_classifier_dt.joblib')
        # predict on the sample tweet text
        prediction = pipeline.predict(df['review'])
        print(prediction)
        df['sentiment'] = prediction
        print(df)
        return df
    def count_sentiment(df):
        labels = list(pd.unique(df['sentiment']))
        counts = df['sentiment'].value_counts()
        counts = list(pd.unique(counts))
        return labels , counts
