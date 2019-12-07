from twython import Twython
import json
import pandas as pd

#creating twitter credentials as a JSON
# CreateTwitterCredentialJSON()
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],creds['ACCESS_TOKEN'],creds['ACCESS_SECRET'])
query = {'q': 'Finland',
            'result_type': 'popular',
            'count': 10,
            'lang': 'en',
            }
# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
df.head(5)




def CreateTwitterCredentialJSON():
    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = "j976pWHrkFM7DKdfpObJyLlQK"
    credentials['CONSUMER_SECRET'] = "GiqKmdlbh1Rz8kJZ1JA0s2kuOtKLNcg1b4nEivYf6MpHfkMdIY"
    credentials['ACCESS_TOKEN'] = "1202117599062085632-2Zoxet3yeeZ4OLnYd1Y581IaWoUXlR"
    credentials['ACCESS_SECRET'] = "gYtM1810SxWDWSdNBwB0LkSdCKxeApL12mBkWKXxvfn71"

    # Save the credentials object to file
    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)

