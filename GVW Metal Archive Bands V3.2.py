import pandas as pd

df=pd.read_csv('C:/Users/GerritV/Documents/GitHub/Archive-Scrapper/bandext.csv')
df['Links'] = df['Links'].replace("<a href='",'',regex=True)
df['Links'] = df['Links'].replace("</a>",'',regex=True)
df['Links'] = df['Links'].replace("'>",'>',regex=True)
df['Status']= df['Status'].replace('</span>','',regex=True)
split =  df['Status'].str.split('>',n=1,expand=True)
df['Status'] = split[1]
df['Genre']=df['Genre'].replace({'early':'','later':'' , ';':'/' , ',': '/'},regex=True)



df[["Band_link",'Band_Name']] =  df['Links'].str.split('>',expand=True)
df['Band_link2']=df['Band_link'].replace('https://www.metal-archives.com/bands/','',regex=True)
Band_Id = df['Band_link2'].str.split('/',n=1,expand=True)
df['Band_Id'] = Band_Id[1]

Gsplit= df['Genre'].str.split('/',n=7,expand=True)
df['genres0'] = Gsplit[0]
df['genres1'] = Gsplit[1]
df['genres2'] = Gsplit[2]
df['genres3'] = Gsplit[3]
df['genres4'] = Gsplit[4]
df['genres5'] = Gsplit[5]
df['genres6'] = Gsplit[6]
df['genres7'] = Gsplit[7]

export = df[['Band_Id',
'Band_Name'
,'Country'
,'Status'
,'genres0'
,'genres1'
,'genres2'
,'genres3'
,'genres4'
,'genres5'
,'genres6'
,'genres7'
,'Band_link'
]]

export.to_csv('bands33.csv', encoding='utf-8')
