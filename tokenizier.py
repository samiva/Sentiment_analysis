from nltk.tokenize import TweetTokenizer
import nltk
import pandas as pd
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def tokenize_tweets(tweet):
    """Get all of the tokens in a set of tweets"""
    twt = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)
    # combine stop words and punctuation
    stop = stopwords.words("english") + list(string.punctuation)

    filtered_sentence = [token.lower() for token in twt.tokenize(tweet)
                         if token.lower() not in stop]
    return(filtered_sentence)


names = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData',
         'Sweden#AllsvenskanUsersID', 'Sweden#SHLUsersIDData']

df = pd.read_csv('./data/' + names[0] + '.csv', header=0,
                 encoding='cp1252')
tokens = []
for index, row in df.iterrows():
    if(index < 400):
        try:
            if(row['lang'] == "en"):
                print(index)
                token = tokenize_tweets(row['text'])
                tokens.append(token)
            else:
                token = tokenize_tweets(row['translated'])
                tokens.append(token)
        except Exception as e:
            print(str(e))
            continue
# print(tokens)
flat_list = [item for sublist in tokens for item in sublist]
tokens_count = Counter(flat_list)
df = pd.DataFrame(tokens_count.most_common(10), columns=['terms', 'frequency'])
df.plot(kind='bar', x='terms')
plt.show()