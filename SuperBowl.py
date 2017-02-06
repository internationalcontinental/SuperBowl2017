# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 14:01:15 2016

@author: Rachael
"""

import sys
import tweepy
from tweepy import OAuthHandler
import pymongo
from datetime import datetime


now = datetime.now()


atoken = "719527275834818561-5hY4KfOhczFYeXA73fn6rDQ0yqSSb6k"
asecret = "37Nd9vWGumY0RukEOaid6H7eAwpHJsWPy86m4G0MS3AGI"
ckey = "bWbdkXRfCtn61tWKgAJPzXMJu"
csecret = "w3bJirguKsOtAmoOzjnySvucLSzerTo1zMTXDkExOU7HqpDfsD"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient().Superbowl

    def on_status(self, status):
        print status.text , "\n"

        data ={}
        data['text'] = status.text
        data['created_at'] = status.created_at
        data['geo'] = status.geo
        data['source'] = status.source
        data['coordinates']=status.coordinates
        data['favourited']=status.favorite_count
        data['followers']=status.user.followers_count


        self.db.SuperbowlTweets.insert(data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['Brady','Goodell','Belichick'])
