# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 12:52:20 2016

@author: jtb4t
"""
import pandas as pd
import re
from dateutil.parser import parse

df = pd.read_csv('sample_data.csv')

#delete unneeded columns for metadata
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

#split the description column to date and job columns
df['Date'] = df.Description.str.split('|').str[0]
df['Job'] = df.Description.str.split('|').str[1]

#delete old Description column
df = df.drop('Description', axis=1)

#rename Title column to Info from Job
df = df.rename(columns={'Title': 'Info From Job'})

#add box and call number columns
df['Location'] = '' ###box number in '' here
df['Call'] = '' ###RG number in '' here

#insert new empty columns for title and subject
Title = pd.Series('')
df.insert(2, 'Title', Title)
Subject_1 = pd.Series('')
df.insert(4, 'Subject 1', Subject_1)
Subject_2 = pd.Series('')
df.insert(5, 'Subject 2', Subject_2)
Subject_3 = pd.Series('')
df.insert(6, 'Subject 3', Subject_3)

#strip whitespace from Job, Date columns
df['Job']= "'" + df['Job'].str.strip()
df['Job']= df['Job'].str.replace('Folder ', '')
df['Date']= df['Date'].str.strip()

#date cleanup
DateCol = []
dates = df['Date'].tolist()
for i in dates:
    if len(str(i)) == 4:
        i = "'" + i
        DateCol.append(i)
    elif re.match('Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec', i):
        i = "'" + parse(i).strftime('%Y-%m')
        DateCol.append(i)
    elif re.match('^[0-9]*$', i):
        i = "'" + parse(i).strftime('%Y-%m-%d')
        DateCol.append(i)
    else:
        i = "'" + i
        DateCol.append(i)

#create a series from the Date1 list. Add it as a column to df        
DateCol = pd.Series(DateCol)
df['Date'] = DateCol


df.to_csv('clean_sample_data.csv', encoding='utf-8')


