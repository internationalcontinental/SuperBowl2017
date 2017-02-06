# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 15:35:12 2016

@author: Rachael
"""
import ast
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

superb = pd.read_csv('D:\Documents\PythonProjects\superbowl.csv')
superb['createdat'] = pd.to_datetime(pd.Series(superb['created_at']))
superb.set_index('createdat', drop=False, inplace=True)
superb.index = superb.index.tz_localize('GMT').tz_convert('EST')
#superb.index = superb.index - DateOffset(hours = 12)
superb.index
superb1m = superb['created_at'].resample('1t', how='count')

"""""

Maps
"""""


locations = pd.read_csv('D:\Documents\PythonProjects\superbowl.csv', usecols=['geo']).dropna()
geos = []
for location in locations.values:
  
  geos.append(ast.literal_eval(location[0])['coordinates'])


sbmap = folium.Map(location=SB_coordinates, zoom_start=4)
lats=[float(item[0]) for item in geos]
longs=[float(item[1]) for item in geos]
sbmap.add_children(plugins.HeatMap(zip(lats, longs), radius = 10))
sbmap.save('sb2017.html')


# initialize and create map
tweet_map = folium.Map(location=SB_coordinates, tiles='Mapbox Bright', zoom_start=7)

# add markers
for geo in geos:
  tweet_map.circle_marker(location=geo, radius=250)

tweet_map.create_map(path='map.html')
"""""
Word frequency
"""""
tokens=[]
stop = stopwords.words('english')
text = superb['text']
for texts in text.values:
  tokens.extend([word.lower().strip(':,."-') for word in texts.split()])

filtered_tokens = [word.translate(None,string.punctuation) for word in tokens]

freq_dist = nltk.FreqDist(filtered_tokens)
print freq_dist.plot(25)




tweets_by_country = superb['source'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Source', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
plt.show()

