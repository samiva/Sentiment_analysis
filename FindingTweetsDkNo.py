from twython import Twython
import json
import pandas as pd
from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile

# oauth = credsfromfile()
# client = Streamer(**oauth)
# client.register(TweetViewer(limit=10))
# client.sample().encode('utf-8')
# tw = Twitter()
# df = pd.read_csv('./data/DenmarkUsersID.csv', header=None)
# df = df.applymap(str)
# x = df.to_string(header=False,
#                  index=False,
#                  index_names=False).split('\n')
# vals = [','.join(ele.split()) for ele in x]
# print(tw.tweet(follow=vals[0], limit=10, stream=False))


with open("twitter_credentials_sentanal.json", "r") as file:
    creds = json.load(file)


python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                        creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
#exclude metalligaen
names = ['Denmark#sldkUsersID','Norway#getligaenUsersID','Norway#eliteserienUsersID']
for n in names:
    df = pd.read_csv('./data/' + n + '.csv', header=None)
    df = df.applymap(str)
    x = df.to_string(header=False,
                    index=False,
                    index_names=False).split('\n')
    vals = [','.join(ele.split()) for ele in x]
    # Query
    query = {'q': '',
            'count': 1,
            }
    dict_ = {'text': [], 'name': [], 'id': [], 'lang': []}
    my_string = ','.join(map(str, vals))

    for i in vals:
        statuses = python_tweets.get_user_timeline(user_id=i, count=50)
        for status in statuses:
            dict_['name'].append(status['user']['screen_name'])
            dict_['id'].append(status['user']['id_str'])

            # cleaning the text from junk characters like emojies except nordic layout
            clean_str = ''.join(
                [c for c in status['text'] if ord(c) < 128 or ord(c) == 228 or ord(c) == 229 or ord(c) == 246])
            dict_['text'].append(clean_str)
            dict_['lang'].append(status['lang'])
        df1 = pd.DataFrame(dict_)
        df1.to_csv('./data/' + n +'Data.csv',
                header=True, index=False, encoding='cp1252')
