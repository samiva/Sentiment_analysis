from googletrans import Translator
import pandas as pd
translator = Translator()
names = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData',
         'Sweden#AllsvenskanUsersID', 'Sweden#SHLUsersIDData']
# df = pd.read_csv('./data/' + 'Finland#liigaUsersIDData' + '.csv', header=0, encoding='cp1252')
# df['translated'] = "null"
# df.to_csv('./data/' + 'Finland#liigaUsersIDData' + '.csv', header=True, encoding='cp1252')

for n in names:
    df = pd.read_csv('./data/' + n + '.csv', header=0,
                     encoding='cp1252')
    print(n)
    for index, row in df.iterrows():
        if(index > 200 and index <= 400):
            translator = Translator()
            if(row['lang'] != 'en'):
                try:
                    txt = translator.translate(
                        row['text'], dest='en', src=row['lang']).text
                    clean_str = ''.join(
                        [c for c in txt if ord(c) < 128 or ord(c) == 228 or ord(c) == 229 or ord(c) == 246])
                    df.loc[index, 'translated'] = clean_str
                except Exception as e:
                    print(str(e))
                    continue

    df.to_csv('./data/' + n + '.csv', header=True,
              index=False, encoding='cp1252')
    break
