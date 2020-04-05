import urllib2,cookielib
import json
import pandas as pd
from sqlalchemy import create_engine
import ctypes
import time
import datetime


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Connection': 'keep-alive'}

site = 'https://www.metal-archives.com/review/ajax-list-browse/by/alpha/selection/'
site2 = '/json/1?sEcho=3&iColumns=7&sColumns=&iDisplayStart='
dbreport = 'metalarchive'
table = 'albumreview'


engine = create_engine("mysql+pymysql://{user}:{pw}@localhost:3306/{db}".format(user="root",pw="", db=dbreport))
data = pd.DataFrame()


Letters = 'a b c d e f g h j k l m n o p q r s t u v w x y z nbr'.split()

for Letter in Letters:
    Number = 0
    Number = str(Number)
    req = urllib2.Request(site+Letter+site2+Number, headers=hdr)
    page = urllib2.urlopen(req)
    content = page.read()

    js = json.loads(content)

    print js['iTotalRecords']
    Aantal = js['iTotalRecords']
    Aantal_batch = (Aantal/200)+1

    soveel = 0

    for i in range(Aantal_batch):
        Number = str(Number)
        for attempt in range(5):
            time.sleep(2)
            try:
                print(Number)
                req = urllib2.Request(site+Letter+site2+Number, headers=hdr)
                page = urllib2.urlopen(req, timeout=8)
                content = page.read()
                js = json.loads(content)

                #print js['aaData']
                df=pd.DataFrame(js['aaData'])
                data = data.append(df)

                Number = int(Number)+200

                rvs = data[1].str.split('"', n = 4, expand = True)
                data['Reviewlink'] = rvs[1]
                data['ReviewTitle'] = rvs[3]
                bs=data[2].str.split('"', n = 2, expand = True)
                data['Bandlink'] = bs[1]
                data['Band_Name'] =bs[2]
                data['Band_Name']= data['Band_Name'].replace('</a>','',regex=True)
                data['Band_Name']= data['Band_Name'].replace('>','',regex=True)

                als = data[3].str.split('"', n = 2, expand = True)
                data['Albumlink'] = als[1]
                data['Album_Name'] = als[2]
                data['Album_Name']= data['Album_Name'].replace('</a>','',regex=True)
                data['Album_Name']= data['Album_Name'].replace('>','',regex=True)
                ur=data[5].str.split('"', n = 2, expand = True)
                data["Reviewer_Link"] = ur[1]

                aln = als[1].str.split('/',n=6, expand=True)
                data["Album_Id"] = aln[6]

                data['ReviewRate'] = data[4]

                frame =data[['Album_Id','Album_Name','Albumlink','Band_Name','Bandlink','ReviewRate','ReviewTitle','Reviewer_Link','Reviewlink']]

                frame.to_sql(table, con=engine, if_exists='append', chunksize=200)

                print('Done '+str((soveel)+1)+' of '+str(Aantal_batch)+' of '+str(Letter))
                soveel += 1
            except:
                print('Attempt', attempt, 'of 5')
                time.sleep(3)
                print('Retrying...')
                continue
            break

ctypes.windll.user32.MessageBoxA(0, "DONE", "Yeahhhh", 1)
