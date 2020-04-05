import urllib2,cookielib
import json
import pandas as pd
from sqlalchemy import create_engine
import ctypes
import time
import datetime


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Connection': 'keep-alive'}

site = 'https://www.metal-archives.com/search/ajax-artist-search'
site2 = '/json/1?sEcho=3&iColumns=4&sColumns=&iDisplayStart='


col_names = ['Artist_link_and_NickName', 'Full_Name_Artist', 'Country_of_Artist', 'Band_link']
data = pd.DataFrame()

Letters = 'a'   #Can just take loop out pointless really

dbreport = 'metalarchive' #MySQL DB
table = 'artist' #Table of DB

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost:3306/{db}".format(user="root",pw="", db=dbreport))
#notice, localhost 3306
#no password


for Letter in Letters: #pointless
    Num = 0         #this is really just incase the scripts has to stop for example internet drop
    Number = Num*200    #part of URL => iDisplayStart
    Number = str(Number)
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    content = page.read()

    js = json.loads(content)

    print js['iTotalRecords']
    Aantal = js['iTotalRecords']
    Aantal_batch = (Aantal/200)+1
    soveel = Num
#yeah all that just to know how much the loop has to go. and keeping track

    for i in range(Aantal_batch):
        Number = str(Number)
        for attempt in range(10):
            time.sleep(2) #this wasnt required for bands by country but for artist of 717k yes.
            try:
                print(Number)
                req = urllib2.Request(site+site2+Number, headers=hdr)
                page = urllib2.urlopen(req, timeout=20) #can make 5 also.

                Number = int(Number)+200
                data.columns = col_names

                AL = data['Artist_link_and_NickName'].str.split('"', n=3, expand =True)
                data["Artist_Link"] = AL[1]

                data['Band_link']= data['Band_link'].replace('&nbsp;','' , regex=True)
                BL = data['Band_link'].str.split('"', n=2, expand = True)
                data['Band_URL'] = BL[1]

                BL[2]=BL[2].replace('</a>', '',regex=True)
                BL[2]=BL[2].replace('>', '',regex=True)
                BL2 = BL[2].str.split(',', n=1, expand =True)

                data['Band_Name'] = BL2[0]

                BI= data['Band_URL'].str.split('/',n=5, expand=True)
                data['Band_Id'] = BI[5]




                frame =data[['Artist_link_and_NickName', 'Full_Name_Artist', 'Country_of_Artist', 'Band_link',"Artist_Link",'Band_URL','Band_Name','Band_Id']]
                #data.to_csv('toetsweer.csv', encoding='utf-8')

                frame.to_sql(table, con=engine, if_exists='append', chunksize=200)
                print('Done '+str(soveel)+' of '+str(Aantal_batch))
                soveel += 1
            except:
                print('Attempt ', attempt, ' of 5.')
                time.sleep(4)
                print('Retrying...')
                continue
            break


ctypes.windll.user32.MessageBoxA(0, "DONE", "Yeahhhh", 1)
