# packages to store and manipulate data
import pandas as pd
import numpy as np

# plotting packages
import matplotlib.pyplot as plt
import seaborn as sns

# model building package
import sklearn

# package to clean text
import re

def is_nan(x):
    return x is np.nan or x!= x

dataset_name = 'Finland#liigaUsersIDData'
# import dataset
df = pd.read_csv('./data/' + dataset_name + '.csv', header=0,
                 encoding='cp1252')

# put translated texts into a list
translated = []
for index, row in df.iterrows():
    if pd.isnull(row['translated']):
        df['is_retweet'] = False
        continue
    else:
        translated.append(row['translated'])
        df['is_retweet'] = 'RT' in row['translated'][:2]
        # if is_nan(df['translated'])==False:

# for tweet in translated:
#     if 'RT' in tweet[:2]:
#         print(tweet)          
# print(len(translated))
# translated = [x for x in translated if x[:2] != 'RT']
# print(len(translated))
# for i in translated:

#     print(i)
# print(df.dtypes)
# print(df.translated.unique().shape)

# column for retweets
# df['is_retweet'] = df['translated'].apply(lambda x:  x[:2] =='RT')
# 10 most repeated tweets
counts = df.groupby(['translated']).size().reset_index(name='counts').counts

# define bins for histogram
my_bins = np.arange(0,counts.max()+2, 1)-0.5

# plot histogram of tweet counts
plt.figure()
plt.hist(counts, bins = my_bins)
plt.xlabels = np.arange(1,counts.max()+1, 1)
plt.xlabel('copies of each tweet')
plt.ylabel('frequency')
plt.yscale('log', nonposy='clip')
plt.show()