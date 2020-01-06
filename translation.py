from googletrans import Translator
import pandas as pd
import numpy as np
import time
from google.cloud import translate


translator = Translator()
names_fi_sw = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData',
               'Sweden#AllsvenskanUsersIDData', 'Sweden#SHLUsersIDData']


# Denmark icehockey league 'metalligaen' excluded since it found only one user
names_dk_no = ['Denmark#sldkUsersIDData',
               'Norway#getligaenUsersIDData', 'Norway#eliteserienUsersIDData']

# add translated column to dataframe
# df = pd.read_csv('./data/' + names_fi[3] +
#                  '.csv', header=0, encoding='cp1252')
# df['translated'] = ""
# df.to_csv('./data/' + names_fi[3] +
#           '.csv', index=False, header=True, encoding='cp1252')

# translate tweets

client = translate.TranslationServiceClient()
parent = client.location_path("driven-lore-264120", "global")
df = pd.read_csv('./data/' + names_dk_no[2] + '.csv', header=0,
                 encoding='cp1252')
for index, row in df.iterrows():
    # time.sleep(0.1)
    # if(index > 1000):
    if(row['lang'] != 'en'):
        try:
            txt = client.translate_text(
                [row['text']], parent=parent, target_language_code='en').translations
            clean_str = ''.join(
                [c for c in txt[0].translated_text if ord(c) < 128 or ord(c) == 228 or ord(c) == 229 or ord(c) == 246])
            df.loc[index, 'translated'] = clean_str
            # print(df.loc[index, 'translated'])
        except Exception as e:
            print(str(e))
            continue
df.to_csv('./data/' + names_dk_no[2] + '.csv', header=True,
          index=False, encoding='cp1252')
