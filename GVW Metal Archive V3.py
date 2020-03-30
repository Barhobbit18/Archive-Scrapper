import urllib2,cookielib
import json
import pandas as pd


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Connection': 'keep-alive'}

site = 'https://www.metal-archives.com/browse/ajax-letter/l/'
site2 = '/json/1?sEcho=3&iColumns=4&sColumns=&iDisplayStart='
site3 = '&iDisplayLength=1000&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_=1519758159154'


col_names = ['Links', 'Country', 'Genre', 'Status']
data = pd.DataFrame()

Letters = 'a b c d e f g h j k l m n o p q r s t u v w x y z nbr'.split()

for Letter in Letters:
    Number = 0
    Number = str(Number)
    req = urllib2.Request(site+Letter+site2+Number+site3, headers=hdr)#, data=json.dumps({'param': 'piyo'}).encode())
    page = urllib2.urlopen(req)
    content = page.read()

    js = json.loads(content)

    print js['iTotalRecords']
    Aantal = js['iTotalRecords']
    Aantal_batch = (Aantal/500)+1

    for i in range(Aantal_batch):
        Number = str(Number)
        req = urllib2.Request(site+Letter+site2+Number+site3, headers=hdr)
        page = urllib2.urlopen(req)
        content = page.read()
        js = json.loads(content)

        print js['aaData']
        df=pd.DataFrame(js['aaData'])
        data = data.append(df)
        Number = int(Number)+500

data.columns = column_names
data.index = range(len(data))

data.to_csv('500a.csv', encoding='utf-8')
