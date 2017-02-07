# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 15:35:12 2016

@author: Peter
"""
import ast
from bs4 import BeautifulSoup
import re
import folium
import string
from folium import plugins
import pandas as pd
from pandas.tseries.resample import TimeGrouper
from pandas.tseries.offsets import DateOffset
import vincent
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
import matplotlib.pyplot as plt


SB_coordinates=(41.6764,-86.25528)  # South Bend coordinates for the map to start at

superb = pd.read_csv('D:\Documents\PythonProjects\SuperBowl2017\superbowl.csv')
superb['createdat'] = pd.to_datetime(pd.Series(superb['created_at']))
superb.set_index('createdat', drop=False, inplace=True)
superb.index = superb.index.tz_localize('GMT').tz_convert('EST')
#superb.index = superb.index - DateOffset(hours = 12)
superb.index
superb1m = superb['created_at'].resample('1t', how='count')

"""""

Maps
"""""


locations = pd.read_csv('D:\Documents\PythonProjects\SuperBowl2017\superbowl.csv', usecols=['geo']).dropna()
loctext=pd.read_csv('D:\Documents\PythonProjects\SuperBowl2017\superbowl.csv', usecols=['geo','text']).dropna()
geos = []
ltext=[]
##for location in locations.values:
##  
##  geos.append(ast.literal_eval(location[0])['coordinates'])
  
for location in loctext.values:
  
  geos.append(ast.literal_eval(location[1])['coordinates'])
  ltext.append(location[0])

sbmap = folium.Map(location=SB_coordinates, zoom_start=4)
lats=[float(item[0]) for item in geos]
longs=[float(item[1]) for item in geos]
sbmap.add_children(plugins.HeatMap(zip(lats, longs), radius = 10))
sbmap.save('sb2017.html')


# initialize and create map
tweet_map = folium.Map(location=SB_coordinates, tiles='Mapbox Bright', zoom_start=7)

# add markers
for geo in geos:
  folium.Marker(location=geo,icon=folium.Icon(color='cloud')).add_to(tweet_map)


tweet_map.save('map.html')


"""""
Tweet source
"""""

tweets_by_source = superb['source'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Source', fontsize=15, rotation=45)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 sources', fontsize=15, fontweight='bold')
tweets_by_source[:5].plot(ax=ax, kind='bar', color='blue')
plt.show()


"""""
Word frequency
"""""

##tokens=[]
##stop = stopwords.words('english')
##text = superb['text']
##for texts in text.values:
##  tokens.extend([word.lower().strip(':,."-') for word in texts.split()])
##
##filtered_tokens = [word.translate(None,string.punctuation) for word in tokens]
##
##freq_dist = nltk.FreqDist(filtered_tokens)
##print freq_dist.plot(25)


"""""
Text analysis
"""""

def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review).get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))

# Get the number of reviews based on the dataframe column size
num_reviews = superb["text"].size

### Initialize an empty list to hold the clean reviews
##clean_superb = []
##
##for i in xrange( 0, num_reviews ):
##    # Call our function for each one, and add the result to the list of
##    # clean reviews
##    clean_superb.append( review_to_words( superb["text"][i] ) )






