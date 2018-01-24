#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 01:17:45 2017

@author: xinan
"""

import json
import sys
import time
import wget
from twython import TwythonStreamer

consumer_key = 'xxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxx'

#Save the data into a json file
MAX_TWEETS = 1000000
OUTPUT = 'data_{}.json'.format(int(time.time()))


class MyStreamer(TwythonStreamer):
    """our own subclass of TwythonStreamer that specifies
    how to interact with the stream"""
    count = 0

    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python object representing a tweet"""

        # only want to collect English-language tweets
        if data['lang'] == 'en':
            
            with open(OUTPUT, 'a') as f:
                f.write(json.dumps(data) + '\n')
            self.count += 1
        
        # stop when we've collected enough
        if self.count >= MAX_TWEETS:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


if __name__ == "__main__":
    keywords_and = ' '.join(sys.argv[1:])

    stream = MyStreamer(consumer_key , consumer_secret,
                        access_token, access_token_secret)
#filter the data with keywords
    stream.statuses.filter(track=['iphone x','iphoneX',])
    
    downloaded = 0
    media_files = set()
    for status in stream:
      media = status.entities.get('media', [])
      if(len(media) > 0):
          wget.download(media[0]['media_url'], out='/Users/xinan/Desktop/big_data')
          downloaded += 1  
          
    
    
    