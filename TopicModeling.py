# packages to store and manipulate data
import pandas as pd
from bokeh.io import push_notebook, show, output_notebook, export_png
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet
output_notebook()

import numpy as np
import re
from gensim import models, corpora
from nltk import word_tokenize
from nltk.corpus import stopwords
from gensim import similarities

from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer


def extract_tweets_dataset(dataset_name):
    # import dataset
    df = pd.read_csv('./data/' + dataset_name + '.csv', header=0,
                    encoding='cp1252')
    data = []
    for index, row in df.iterrows():
        if pd.isnull(row['translated']):
            continue
        else:
            data.append(row['translated'])

    # Remove retweets
    data = [x for x in data if x[:2] != 'RT']

    data = list(map(lambda x: re.sub(r'http\S+', '', x), data))
    for i in data:
        print(i)
    return data
 
def clean_text(text):
    tokenized_text = word_tokenize(text.lower())
    cleaned_text = [t for t in tokenized_text if t not in STOPWORDS and re.match(r'[a-zA-Z\-][a-zA-Z\-]{2,}', t) ]
    return cleaned_text

savepath ='./data/'

dataset_names = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData', 
                'Sweden#SHLUsersIDData', 'Sweden#AllsvenskanUsersIDData',
                'Norway#getligaenUsersIDData', 'Norway#eliteserienUsersIDData',
                'Denmark#sldkUsersIDData']

NUM_TOPICS = 20
STOPWORDS = stopwords.words('english')
if __name__=='__main__':
    for dataset_name in dataset_names:
        print(dataset_name)
        data = extract_tweets_dataset(dataset_name)
        # For gensim we need to tokenize the data and filter out stopwords
        tokenized_data = []
        for text in data:
            tokenized_data.append(clean_text(text))
        print(len(tokenized_data))
        # Build a Dictionary - association word to numeric id
        dictionary = corpora.Dictionary(tokenized_data)
        
        # Transform the collection of texts to a numerical form
        corpus = [dictionary.doc2bow(text) for text in tokenized_data]
        
        # Have a look at how the 20th document looks like: [(word_id, count), ...]
        print(corpus[5])
        # [(12, 3), (14, 1), (21, 1), (25, 5), (30, 2), (31, 5), (33, 1), (42, 1), (43, 2),  ...
        # uncomment these to get consistent values everytime between runs
        """ FIXED_SEED = 50
        np.random.seed(FIXED_SEED) """
        # Build the LDA model
        lda_model = models.LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)
        
        # # Build the LSI model
        # lsi_model = models.LsiModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)

        print("LDA Model:")
        
        for idx in range(NUM_TOPICS):
            # Print the first 10 most representative topics
            print("Topic #%s:" % idx, lda_model.print_topic(idx, 10))
        
        print("=" * 20)
        
        """ text = 'league standings'
        bow = dictionary.doc2bow(clean_text(text))
        lda_index = similarities.MatrixSimilarity(lda_model[corpus])
        
        # Let's perform some queries
        similarities = lda_index[lda_model[bow]]
        # Sort the similarities
        similarities = sorted(enumerate(similarities), key=lambda item: -item[1])
        
        # Top most similar documents:
        print(similarities[:10])
        # [(104, 0.87591344), (178, 0.86124849), (31, 0.8604598), (77, 0.84932965), (85, 0.84843522), (135, 0.84421808), (215, 0.84184396), (353, 0.84038532), (254, 0.83498049), (13, 0.82832891)]
        
        # Let's see what's the most similar document
        document_id, similarity = similarities[0]
        print(data[document_id][:1000]) """

        vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
                                    stop_words='english', lowercase=True, 
                                    token_pattern=r'[a-zA-Z\-][a-zA-Z\-]{2,}')
        data_vectorized = vectorizer.fit_transform(data)

        svd = TruncatedSVD(n_components=2)
        documents_2d = svd.fit_transform(data_vectorized.T)
        
        df = pd.DataFrame(columns=['x', 'y', 'document'])
        print(df['document'].head(5 ))
        df['x'], df['y'], df['document'] = documents_2d[:,0], documents_2d[:,1], vectorizer.get_feature_names()
        
        source = ColumnDataSource(ColumnDataSource.from_df(df))
        labels = LabelSet(x="x", y="y", text="document", y_offset=8,
                        text_font_size="8pt", text_color="#555555",
                        source=source, text_align='center')
        
        plot = figure(plot_width=600, plot_height=600)
        plot.circle("x", "y", size=12, source=source, line_color="black", fill_alpha=0.8)
        plot.add_layout(labels)
        export_png(plot, filename=savepath + dataset_name + '.png')
        