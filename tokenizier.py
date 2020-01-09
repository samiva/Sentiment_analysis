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
import operator


def tokenize_tweets(tweet):
    """Get all of the tokens in a set of tweets"""
    twt = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)
    # combine stop words and punctuation
    stop = stopwords.words("english") + list(string.punctuation)
    # ReTweets
    stop.append('rt')
    filtered_sentence = [token.lower() for token in twt.tokenize(tweet)
                         if token.lower() not in stop]
    return(filtered_sentence)


names_fi_sw = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData',
               'Sweden#AllsvenskanUsersIDData', 'Sweden#SHLUsersIDData']
names_dk_no = ['Denmark#sldkUsersIDData',
               'Norway#getligaenUsersIDData', 'Norway#eliteserienUsersIDData']


def _create_frequency_matrix(tweet):
    frequency_matrix = {}
    for token in tweet:
        if token in frequency_matrix:
            frequency_matrix[token] += 1
        else:
            frequency_matrix[token] = 1
    return frequency_matrix


def _create_frequency_matrix_per_organiztion(freq_matrix):
    organization_frequency_matrix = {}

    for doc in freq_matrix:
        for token, frequency in doc.items():
            if token in organization_frequency_matrix:
                organization_frequency_matrix[token] += frequency
            else:
                organization_frequency_matrix[token] = 1

    return organization_frequency_matrix


# number of documents that contains tokens
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


def GetFreqMat(address):
    result = Tokenize(address)
    list1 = (sorted(result['freq_org'].items(),
                    key=lambda item: item[1], reverse=True))
    print(list1)
    df = pd.DataFrame(list1[0:10],
                      columns=['terms', 'frequency'])
    df.plot(kind='barh', x='terms', y='frequency')
    plt.show()


def Tokenize(address):
    df = pd.read_csv(address, header=0,
                     encoding='cp1252')
    mwe_tokenizer = MWETokenizer([('new', 'york')])
    tokens = []
    frequency_matrix = []
    frequency_matrix_organization = {}
    tf_matrix = {}
    idf_matrix = {}
    tf_idf_matrix = {}
    for index, row in df.iterrows():
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

        except Exception as e:
            # print(index)
            # print(str(e))
            continue
    tf_matrix = _create_tf_matrix(frequency_matrix)
    idf_matrix = _create_idf_matrix(tf_matrix, len(df.index))
    tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
    frequency_matrix_organization = _create_frequency_matrix_per_organiztion(
        frequency_matrix)
    print(idf_matrix)
    print(tf_idf_matrix)

    print(frequency_matrix_organization)
    # print(frequency_matrix_organization)
    # print(frequency_matrix)
    # print(tf_matrix)
    # size of the dataframe
    # print(len(df.index))
    # print(sorted(tf_matrix.items(), key=lambda item: item[1], reverse=True))
    # list1 = (sorted(frequency_matrix_organization.items(),
    #                 key=lambda item: item[1], reverse=True))
    # print(list1)
    # flat_list = [item for sublist in tokens for item in sublist]
    # print(flat_list)
    # tokens_count = Counter(flat_list)
    return {"freq_org": frequency_matrix_organization,
            "tf": tf_matrix,
            "idf": idf_matrix,
            "tf_idf": tf_idf_matrix}


if __name__ == '__main__':
    Tokenize('./data/' + names_dk_no[1] + '.csv')
