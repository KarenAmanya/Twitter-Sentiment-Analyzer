from fetch_tweets import *
import pandas as pd
import numpy as np
import re
import psycopg2
import random


#To generate code numbers for each twitter account that will be queried and stored in the database

codes=[]
def generate_code():
    AC_CODE=random.randint(0,100000000)
    if AC_CODE not in codes:
        codes.append(AC_CODE)
    else:
        while AC_CODE in codes:
            generate_code()
    return AC_CODE

#Json to Database
def store_tweets():
    try:
        conn=psycopg2.connect(dbname='',user='', password='',port=5432)#establish connection with db
        cursor=conn.cursor()
        name=f'Account_{generate_code()}' 
        create_script=f""" CREATE TABLE IF NOT EXISTS {name} (
                                                                user_id  VARCHAR(500) ,
                                                                text VARCHAR (500)
                                                                )"""
        cursor.execute(create_script)

        insert_script=f""" INSERT INTO {name} (user_id,text) VALUES (%s,%s)"""
        #Load tweets from json file 
        Data_file=open('Account.json')
        All_tweets=json.load(Data_file)
        for tweet in All_tweets['data']:
            id=int(tweet['id'])
            text=tweet['text']
            #To insert the values to the table
            insert_values=[(id,text)]
            for value in insert_values:
                cursor.execute(insert_script,value)

        conn.commit()
        return name

    except Exception as error:
        print(error)


#Get data from df table
def retrieve_tweets(table_name):
    conn=psycopg2.connect(dbname='t',
    user='',
    password='',
    port=5432)
    cursor=conn.cursor()

    select_table_query=F"select text from {table_name}"
    cursor.execute(select_table_query)
    tweets=cursor.fetchall()
    return tweets

#Fetch tweet column from database and create a dataframe
def create_df(table_name):
    data=retrieve_tweets(table_name)
    cols=['tweet']
    df=pd.DataFrame(data,columns=cols)
    return df

#To clean the tweets 
clean_tweets=[]
def clean_data(Data):
    for tweet in Data.text:
        tweet=re.sub("@[A-Za-z0-9]+", repl=' ',string=tweet)#removes @username/mentions
        tweet=re.sub('[^a-zA-Z]', repl=' ',string=tweet)#removes punctuations + special chars
        tweet=re.sub('(?:(https|http)\s?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)* ',repl=' ',string=tweet)#removes links
        clean_tweets.append(tweet)
    Data['text']=pd.Series(clean_tweets)
    return Data
