from twython import Twython
import json
import pandas as pd
from nltk.twitter import Twitter


def FindUsers(query, country):
    # Search tweets
    dict_ = {'user': [], 'date': [], 'full_text': [],
             'favorite_count': [], 'lang': []}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        # cleaning the text from junk characters like emojies except nordic layout
        clean_str = ''.join(
            [c for c in status['full_text'] if ord(c) < 128 or ord(c) == 228 or ord(c) == 229 or ord(c) == 246])
        dict_['full_text'].append(clean_str)
        dict_['lang'].append(status['lang'])
        dict_['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    print(df.size)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    df.head(5).to_csv('./data/' + country + 'Data.csv', mode='a',
                      header=False, index=False, encoding='windows-1252')
    df.drop_duplicates(subset='user', keep='first', inplace=True)
    df.head(5).to_csv('./data/' + country + 'Users.csv', columns=['user'], mode='a',
                      header=False, index=False, encoding='windows-1252')


def RemoveDuplicates(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(inplace=True)
    df.to_csv(filename, header=False, index=False)


def FindClubUsers(query, clubs, lang, league, country):
    query['q'] = league
    query['lang'] = lang
    print(query['q'] + '\t' + query['lang'])
    FindUsers(query, country)
    query['lang'] = 'en'
    print(query['q'] + '\t' + query['lang'])
    FindUsers(query, country)
    for f in clubs:
        query['q'] = league + ' ' + f
        query['lang'] = lang
        print(query['q'] + '\t' + query['lang'])
        FindUsers(query, country)
        query['lang'] = 'en'
        print(query['q'] + '\t' + query['lang'])
        FindUsers(query, country)
    RemoveDuplicates('./data/' + country + 'Users.csv')


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


# creating twitter credentials as a JSON
# CreateTwitterCredentialJSON()

# Query q
FinlandFootballClubs = ['#HJKHelsinki', '#KuPS', '#honka',
                        '#TurkuPS', '#TampereUnited', '#PK35Vantaa']
SwedenFootballClubs = ['#ifkgbg', '#malmo_ff', 'aik', ]

FinlandLeague = '#Veikkausliiga'
SwedenLeague = '#Allsvenskan'
# Reading the credentials
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)


python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                        creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])


# Query
query = {'q': '',
         'count': 50,
         'tweet_mode': 'extended',
         'lang': ''
         }
FindClubUsers(query, FinlandFootballClubs,
              'fi', FinlandLeague, 'Finland')
FindClubUsers(query, SwedenFootballClubs, 'sv', SwedenLeague, 'Sweden')
