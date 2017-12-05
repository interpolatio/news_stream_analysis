import os
import re
import pandas as pd
import pymorphy2
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def init_text():
    #path = 'D:\\Documents\\python\\russian_text\\all'
    text = []
    if (os.path.exists('all')):
        if os.listdir('all'):
            listdir = os.listdir('all')
            for dir_name in listdir:
                f = open('all\\' + dir_name)
                text.append(f.read())
                f.close()
    return text

def filter_symbol(text):
    text_not_prep = []

    for topic in text:
        text_not_prep.append(re.sub(r'[^\w]', ' ', topic))

    return text_not_prep

def stemming(text_not_prep):
    morph = pymorphy2.MorphAnalyzer()
    text_stem = []
    for line in text_not_prep:
        text_stem.append([morph.parse(t)[0].normal_form for t in line.split()])

    return text_stem

def filter_stop_words(text_stem):
    stops = stopwords.words('russian')
    stops.append('риа')
    stops.append('это')
    stops.append('который')
    stops.append('новость')
    texts_without_stopwords = [[word for word in line if word not in stops] for line in text_stem]
    return texts_without_stopwords

def MDS(texts_without_stopwords):
    data = []
    for i in texts_without_stopwords:
        data.append(" ".join(i))

    vec = CountVectorizer(min_df=10)
    X = vec.fit_transform(data)
    vocab = vec.get_feature_names()

    dist = 1 - cosine_similarity(X)

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    pos = pos * 100

def get_dataframe():

    with open('c:\\data_frame.dat', 'rb') as f:
        dataframe = pickle.load(f)
    return dataframe