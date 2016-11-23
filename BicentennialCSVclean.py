# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 12:52:20 2016

@author: jtb4t
"""
import pandas as pd
import re
from dateutil.parser import parse

df = pd.read_csv('sample_data.csv')

df = df.drop('Tech meta type', axis=1)
df = df.drop('Filesize', axis=1)
df = df.drop('Date archived', axis=1)
df = df.drop('Updated at', axis=1)
df = df.drop('Transcription text', axis=1)
df = df.drop('Desc metadata', axis=1)
df = df.drop('Discoverability', axis=1)
df = df.drop('Md5', axis=1)
df = df.drop('Date dl ingest', axis=1)
df = df.drop('Date dl update', axis=1)
df = df.drop('Creator death date', axis=1)
df = df.drop('Creation date', axis=1)
df = df.drop('Primary author', axis=1)
df = df.drop('Created at', axis=1)
df = df.drop('Dpla', axis=1)

df['Date'] = df.Description.str.split('|').str[0]
df['Job'] = df.Description.str.split('|').str[1]

df = df.drop('Description', axis=1)

df = df.rename(columns={'Title': 'Info From Job'})

df['Location'] = '' ###box number in '' here
df['Call'] = '' ###RG number in '' here

Title = pd.Series('')
df.insert(2, 'Title', Title)
Subject_1 = pd.Series('')
df.insert(4, 'Subject 1', Subject_1)
Subject_2 = pd.Series('')
df.insert(5, 'Subject 2', Subject_2)
Subject_3 = pd.Series('')
df.insert(6, 'Subject 3', Subject_3)

df['Job']= "'" + df['Job'].str.strip()
df['Job']= df['Job'].str.replace('Folder ', '')
df['Date']= df['Date'].str.strip()

#date cleanup
DateCol = []
dates = df['Date'].tolist()
for i in dates:
    if len(i) == 4:
        i = "'" + i
        DateCol.append(i)
    elif re.match('Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec', i):
        i = "'" + parse(i).strftime('%Y-%m')
        DateCol.append(i)
    elif list(i).count('-') == 1:
        i = "'" + parse(i).strftime('%Y-%m')
        DateCol.append(i)
    else:
        i = "'" + parse(i).strftime('%Y-%m-%d')
        DateCol.append(i)
        
DateCol = pd.Series(DateCol)
df['Date'] = DateCol


df.to_csv('clean_sample_data.csv', encoding='utf-8')


