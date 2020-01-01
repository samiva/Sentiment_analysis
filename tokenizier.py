from nltk.tokenize import TweetTokenizer
import nltk
import pandas as pd
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import MWETokenizer
import math as math


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


def _create_frequency_matrix(tweet):
    frequency_matrix = {}
    for token in tweet:
        if token in frequency_matrix:
            frequency_matrix[token] += 1
        else:
            frequency_matrix[token] = 1
    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    tf_matrix = {}
    for doc in freq_matrix:
        for word, frequency in doc.items():
            if word in tf_matrix:
                tf_matrix[word] += 1
            else:
                tf_matrix[word] = 1

    return tf_matrix


def _create_idf_matrix(tf_matrix, total_documents):
    idf_matrix = {}

    for word, frequency in tf_matrix.items():
        idf_matrix[word] = math.log10(
            total_documents / float(frequency))

    return idf_matrix


def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (word1, value1), (word2, value2) in zip(tf_matrix.items(),
                                                idf_matrix.items()):  # here, keys are the same in both the table
        tf_idf_matrix[word1] = float(value1 * value2)

    return tf_idf_matrix


df = pd.read_csv('./data/' + names[0] + '.csv', header=0,
                 encoding='cp1252')

mwe_tokenizer = MWETokenizer([('new', 'york')])
tokens = []
frequency_matrix = []
tf_matrix = {}
idf_matrix = {}
tf_idf_matrix = {}
for index, row in df.iterrows():
    if(index < 400):
        try:
            if(pd.isnull(row['translated'])):
                token = tokenize_tweets(row['text'])
                # link to the tweeter is removed
                token.pop()
                # composed words
                new_token = mwe_tokenizer.tokenize(token)
                tokens.append(new_token)
                # frequency matrix
                frq_matrix = _create_frequency_matrix(new_token)
                frequency_matrix.append(frq_matrix)
                # tf_matrix.append(_create_tf_matrix(frq_matrix))
            else:
                token = tokenize_tweets(row['translated'])
                # link to the tweeter is removed
                token.pop()
                # composed words
                new_token = mwe_tokenizer.tokenize(token)
                tokens.append(new_token)
                # frequency matrix
                frq_matrix = _create_frequency_matrix(new_token)
                frequency_matrix.append(frq_matrix)
                # tf_matrix.append(_create_tf_matrix(frq_matrix))

        except Exception as e:
            print(index)
            print(str(e))
            continue
tf_matrix = _create_tf_matrix(frequency_matrix)
idf_matrix = _create_idf_matrix(tf_matrix, 400)
tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
print(tf_matrix)
print(idf_matrix)
print(tf_idf_matrix)
# size of the dataframe
# print(len(df.index))
# print(frequency_matrix)
# print(tf_matrix)
flat_list = [item for sublist in tokens for item in sublist]
tokens_count = Counter(flat_list)
df = pd.DataFrame(tokens_count.most_common(10), columns=['terms', 'frequency'])
df['frequency'] = df['frequency'].apply(lambda x: (x / 400) * 100)
print(df)
df.plot(kind='barh', x='terms', y='frequency')
plt.show()
