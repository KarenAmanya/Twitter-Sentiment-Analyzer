import tweepy 
import requests
import pandas as pd
import rfc3339 as RF
import json

consumer_key='YOUR CONSUMER KEY'
consumer_secret_key='YOUR CONSUMER SECRET KEY'
Bearer_token='YOUR BEARER TOKEN'
access_token='YOUR ACCESS TOKEN'
access_token_secret='YOUR ACCESS TOKEN SECRET'

callback_uri='oob'
#To create the authentication object
auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key,callback_uri)
acc_url='https://api.twitter.com/2/tweets/search/recent?'
hashtag_url='https://api.twitter.com/1.1/search/tweets.json?'
#To set the access token and secret
auth.set_access_token(access_token,access_token_secret)
#To create the API object
api=tweepy.API(auth,wait_on_rate_limit=True)

#To create a header
def create_header(bearer_token):
    headers={'Authorization': f"Bearer {bearer_token}"}
    return headers

#To create parameters
def create_parameters(handle,From,To,Items):
    parameters={'query':handle,
                'start_time':RF.format(pd.to_datetime(From)),
                'end_time':RF.format(pd.to_datetime(To)),
                'max_results':Items,
                }
    return parameters


#To request data from an account and  store the result in a json file
def Get_tweets(Parameters,Headers):
    with open('Account.json',mode='w') as data_file:
        response_1=requests.get(acc_url,params=Parameters,headers=Headers).json()
        json.dump(response_1,data_file)

def Fetch_tweets(Account,start_date,end_date):
    Headers=create_header(Bearer_token)
    Parameters=create_parameters(handle=Account,From=start_date,To=end_date,Items=100)
    Get_tweets(Parameters=Parameters,Headers=Headers)
    
