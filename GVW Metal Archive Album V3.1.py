import urllib2,cookielib
import json
import pandas as pd
from sqlalchemy import create_engine
import ctypes
import time
import datetime


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Connection': 'keep-alive'}

site = 'https://www.metal-archives.com/search/ajax-advanced/searching/albums%20/%20/?&releaseYearFrom=1900&releaseMonthFrom=0&releaseYearTo=2021%20\%20&releaseMonthTo=12&_=1&sEcho=0&iColumns=4&sColumns=&iDisplayStart='


col_names = ['Band_link', 'album_name', 'Type', 'DateRelease']
data = pd.DataFrame()

Letters = 'a'   #Can just take loop out pointless really

dbreport = 'metalarchive' #MySQL DB
table = 'albums' #Table of DB

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost:3306/{db}".format(user="root",pw="", db=dbreport))
#notice, localhost 3306
#no password


for Letter in Letters: #pointless
    Num = 0      #this is really just incase the scripts has to stop for example internet drop
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
        for attempt in range(3):
            time.sleep(1)
            try:

                Number = str(Number)
                req = urllib2.Request(site+Number, headers=hdr)
                page = urllib2.urlopen(req, timeout=5).
                content = page.read()
                js = json.loads(content)
                data=pd.DataFrame(js['aaData'])

                Number = int(Number)+200

                new = data[0].str.split('|',n=1,expand = True)
                data[4] =new[0]


                data[4]=data[4].replace('<a href="https://www.metal-archives.com/bands/', '',regex=True)
                data[4]=data[4].replace('</a>', '',regex=True)
                data[4]=data[4].replace('title="', '>',regex=True)
                data[4]=data[4].replace('"', '',regex=True)
                data[4]=data[4].replace('/', '>',regex=True)
                data [['Band2','Band_Id','Band_Country','Band_Name']] = data[4].str.split('>', expand=True)

                data[9] = data[1]
                data[9]=data[9].replace('<a href="https://www.metal-archives.com/albums/', '',regex=True)
                data[9]=data[9].replace('<!-- 1 -->', '',regex=True)
                data[9]=data[9].replace('</a>', '',regex=True)
                data[9]=data[9].replace('">', '/',regex=True)
                split = data[9].str.split('/',n=3, expand=True)
                data['Album_ID'] = split[2]
                data['Album_Name'] = split[3]

                data['yearCon'] = data[3]
                data [['Year','FullDate']] = data['yearCon'].str.split('<', expand=True)
                data['FullDate']= data['FullDate'].replace('!--','',regex=True)
                data['FullDate']= data['FullDate'].replace('-->','',regex=True)
                data['Year'] = data['FullDate'].str[:5]
                data['Type'] = data[2]

                frame =data[['Band_Id','Band_Name','Album_ID', 'Album_Name', 'Type', 'Year','FullDate']]

                frame.to_sql(table, con=engine, if_exists='append', chunksize=200)
                print('Done '+str(soveel)+' of '+str(Aantal_batch))
                soveel += 1
            except:
                print('Attempt ', attempt, ' of 3.')
                time.sleep(3)
                print('Retrying...')
                continue
            break



ctypes.windll.user32.MessageBoxA(0, "Album Done", "Yeahhhh", 1)
