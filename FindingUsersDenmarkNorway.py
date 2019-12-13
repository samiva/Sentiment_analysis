from twython import Twython
import json
import pandas as pd
from nltk.twitter import Twitter


def FindUsers(query, country, league):
    # Search tweets
    dict_ = {'user': [],
             'favorite_count': [], 'id': []}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['id'].append(status['user']['id_str'])
        dict_['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    print(df.size)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    # df.head(5).to_csv('./data/' + country + 'Data.csv', mode='a',
    #                   header=False, index=False, encoding='utf-8')
    df.drop_duplicates(subset='id', keep='first', inplace=True)
    df.head(5).to_csv('./data/' + country + league + 'Users.csv', columns=['user'], mode='a',
                      header=False, index=False, encoding='utf-8')
    df.head(5).to_csv('./data/' + country + league + 'UsersID.csv', columns=['id'], mode='a',
                      header=False, index=False, encoding='utf-8')


def RemoveDuplicates(filename):
    df = pd.read_csv(filename, header=None)
    df.drop_duplicates(inplace=True)
    df.to_csv(filename, header=False, index=False, encoding='utf-8')


def FindClubUsers(query, clubs, lang, league, country):
    query['q'] = league
    query['lang'] = lang
    print(query['q'] + '\t' + query['lang'])
    FindUsers(query, country, league)
    query['lang'] = 'en'
    print(query['q'] + '\t' + query['lang'])
    FindUsers(query, country, league)
    for f in clubs:
        query['q'] = f
        query['lang'] = lang
        print(query['q'] + '\t' + query['lang'])
        FindUsers(query, country, league)
        query['q'] = league + ' ' + f
        query['lang'] = lang
        print(query['q'] + '\t' + query['lang'])
        FindUsers(query, country, league)
        query['lang'] = 'en'
        print(query['q'] + '\t' + query['lang'])
        FindUsers(query, country, league)
    RemoveDuplicates('./data/' + country + league + 'Users.csv')


def FindUserIDByName(filename):
    df = pd.read_csv(filename, header=None)
    df = df.applymap(str)
    x = df.to_string(header=False,
                     index=False,
                     index_names=False).split('\n')
    vals = [','.join(ele.split()) for ele in x]
    # Query
    query = {'q': '',
             'count': 1,
             }
    dict_ = {'user': []}
    my_string = ','.join(map(str, vals))
    users = python_tweets.lookup_user(screen_name=my_string)
    for user in users:
        dict_['user'].append(user['id_str'])
    df1 = pd.DataFrame(dict_)
    df1.to_csv('./data/DenmarkUsersID.csv', columns=['user'],
               header=False, index=False, encoding='uft-8')


def CreateTwitterCredentialJSON():
    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = "j976pWHrkFM7DKdfpObJyLlQK"
    credentials['CONSUMER_SECRET'] = "GiqKmdlbh1Rz8kJZ1JA0s2kuOtKLNcg1b4nEivYf6MpHfkMdIY"
    credentials['ACCESS_TOKEN'] = "1202117599062085632-2Zoxet3yeeZ4OLnYd1Y581IaWoUXlR"
    credentials['ACCESS_SECRET'] = "gYtM1810SxWDWSdNBwB0LkSdCKxeApL12mBkWKXxvfn71"

    # Save the credentials object to file
    with open("twitter_credentials_sentanal.json", "w") as file:
        json.dump(credentials, file)


# creating twitter credentials as a JSON
CreateTwitterCredentialJSON()

# Query q
DenmarkFootballClubs = ['#achorsens', '#Brøndby', '#aabfcn',
                        '#HobroIK', '#randersfc', '#fcklive']
NorwayFootballClubs = ['#ifkgbg', '#malmo_ff', 'aik', ]
NorwayIceHockeyClubs = ['#frölunda', '#Färjestad', 'Brynäs', 'Luleå']

DenmarkIceHockeyClubs = ['#HPK', '#Kärpät', '#jypliiga']

DenmarkLeague = '#sldk'
DenmarkIceHockeyLeague = '#liiga'

NorwayLeague = '#Allsvenskan'
NorwayIceHockeyLeague = '#SHL'

# Reading the credentials
with open("twitter_credentials_sentanal.json", "r") as file:
    creds = json.load(file)


python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                        creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])


# Query
query = {'q': '',
         'count': 50,
         'tweet_mode': 'extended',
         'lang': ''
         }
print("Football")
# FindClubUsers(query, DenmarkFootballClubs,
#               'fi', DenmarkLeague, 'Denmark')
# FindClubUsers(query, NorwayFootballClubs, 'sv', NorwayLeague, 'Norway')
# print("Ice Hokey")
# FindClubUsers(query, DenmarkIceHockeyClubs,
#               'fi', DenmarkIceHockeyLeague, 'Denmark')
# FindClubUsers(query, NorwayIceHockeyClubs,
#               'sv', NorwayIceHockeyLeague, 'Norway')

# RemoveDuplicates('./data/' + 'Denmark' + DenmarkLeague + 'Users.csv')
# RemoveDuplicates('./data/' + 'Norway' + DenmarkLeague + 'Users.csv')
# RemoveDuplicates('./data/' + 'Denmark' + 'UsersID.csv')
# RemoveDuplicates('./data/' + 'Norway' + 'UsersID.csv')


# FindUserIDByName('./data/DenmarkUsers.csv')
