
"""
Created on Thu Nov 30 16:14:08 2017

@author: xinan
"""

#This is the main program of sentiment analysis
#The keyword is 'iPhone X' when we collect data


"""
I will have the sentiment analysis on iphone x using the 
twitter data which I collect through the twitter API. 
Then, I create a pandas dataframe for this data to exract 
the tweets by some new features's key words, including
"all screen", "wireless charging", "face id", "camera"
and "animoji". And analyze which is the hottest new feature and
how is twitter users' attitudes on those features.


"""

#All neccesary libraries
from collections import defaultdict
import json
import pandas as pd
import re
from textblob import TextBlob
from matplotlib import pyplot as plt

#Define the sentiment lable by the polarity. 
def get_sentiment(polarity):
    if polarity < 0:
        return "negative"
    elif polarity == 0:
        return "neutral"
    else:
        return "positive"

#This function will extract the tweets the new features of iphone x.
'''
The regular expression operations libray is used here to scan the strings
in the twitter data,find and reture the match items, which I am searching.


'''

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        print ('Match Found')
        return text #return the word instead of text when counting new features keywords
    else:
        print ('Match not found')
        return ''

if __name__ == "__main__":
    
    #Reading in all twitter data, which are stored in data.json
    tweets_data_path = '/Users/xinan/Desktop/big_data/data.json'
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    #Try and except clause help us skip the line with unreadble data
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
         
    #Now the twitter data have been transferd in tweets_data variable
    
    
    #Creating a pandas dataframe with the tweets
    tweets = pd.DataFrame()
    index = 0
    for num, line in enumerate(tweets_data):
        try:
            print (num,line['text'])
            tweets.loc[index,'text'] = line['text']
            index = index + 1 
        except:
            print (num, "line not parsed")
        continue
    
    #Adding each new features as a column to the tweets DataFrame
    '''
    The key words include all screen, wireless charging. face id, camera and animoji.
    In order to express and recognize the specific phrases, like "all screen". 
    We have to convert them into the following format: (^|)(word1( word2)?)( |$)
    
    '''
    print ('Adding features tags to the data\n')
    tweets['(^|)(all( screen)?)( |$)'] = tweets['text'].apply(lambda tweet: word_in_text('(^|)(all( screen)?)( |$)', tweet))
    tweets['(^|)(wireless( charging)?)( |$)'] = tweets['text'].apply(lambda tweet: word_in_text('(^|)(wireless( charging)?)( |$)', tweet))
    tweets['(^|)(face( id)?)( |$)'] = tweets['text'].apply(lambda tweet: word_in_text('(^|)(face( id)?)( |$)', tweet))
    tweets['camera'] = tweets['text'].apply(lambda tweet: word_in_text('camera', tweet))
    tweets['animoji'] = tweets['text'].apply(lambda tweet: word_in_text('animoji', tweet))
    
    #Analyzing Tweets by new features by counting the times that they were mentioned in tweets
    
    print ('Analyzing tweets by iphone x new features\n')
    prg_langs = ['all screen', 'wireless charging', 'face id','new camera', 'animoji']
    tweets_by_prg_lang = [tweets['(^|)(all( screen)?)( |$)'].value_counts()[True], 
                                 tweets['(^|)(wireless( charging)?)( |$)'].value_counts()[True], 
                                 tweets['(^|)(face( id)?)( |$)'].value_counts()[True],
                                 tweets['camera'].value_counts()[True],
                                 tweets['animoji'].value_counts()[True]]
                                                                
    x_pos = list(range(len(prg_langs)))
    width = 0.4
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Popularity of new features ', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    plt.savefig('tweet_by_prg_language_1', format='png')

    
    #sentiments analysis for all twitter data(iphone x)
    '''
    We used .sentiment.polarity function from Textblob library  
    to help us achieve sentiments analysis. And we convert the
    polarity in to our defined lables by get_sentiment function,
    whihch we created before
    '''
    sentiments = defaultdict(set)

    for tw in tweets_data:
        text = dict(tw)['text'].lower()
        blob = TextBlob(text)
        sent = get_sentiment(blob.sentiment.polarity)
        
        sentiments[sent].add(text)
     
    total = sum(len(i) for i in sentiments.values())

    perc_pos = len(sentiments["positive"]) / total * 100
    perc_neg = len(sentiments["negative"]) / total * 100
    perc_neu = len(sentiments["neutral"]) / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for iphone x')
    plt.show()
    
    #sentiments analysis for new features
    
    #sentiments analysis for all screen
    '''
    Convert the pandas dataframe back to json format by the colunm that we 
    are going to analyze
    '''
    featext=tweets['(^|)(all( screen)?)( |$)'] .to_json()
    
    '''
    sentiments analysis by textblob
    '''
    
    zen = TextBlob(featext)
    
    feature = []
    for sentence in zen.sentences:
        sentx = get_sentiment(sentence.sentiment.polarity)
        feature.append(sentx)    
        
    total = len(zen.sentences)
    perc_pos = feature.count("positive") / total * 100
    perc_neg = feature.count("negative") / total * 100
    perc_neu = feature.count("neutral") / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for all screen')
    plt.show()
    
    
    
    #sentiments analysis for wireless charging
    #same function as previous feature analytics
    featext=tweets['(^|)(wireless( charging)?)( |$)'] .to_json() 
    zen = TextBlob(featext)
    feature = []
    for sentence in zen.sentences:
        sentx = get_sentiment(sentence.sentiment.polarity)
        feature.append(sentx)  
        
    total = len(zen.sentences)
    perc_pos = feature.count("positive") / total * 100
    perc_neg = feature.count("negative") / total * 100
    perc_neu = feature.count("neutral") / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for wireless charging')
    plt.show()
    
    #sentiments analysis for face id
    #same function as previous feature analytic
    featext=tweets['(^|)(face( id)?)( |$)'] .to_json() 
    zen = TextBlob(featext)
    feature = []
    for sentence in zen.sentences:
        sentx = get_sentiment(sentence.sentiment.polarity)
        feature.append(sentx)  
        
    total = len(zen.sentences)
    perc_pos = feature.count("positive") / total * 100
    perc_neg = feature.count("negative") / total * 100
    perc_neu = feature.count("neutral") / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for face id')
    plt.show()
    
    #sentiments analysis for camera
    #same function as previous feature analytic
    featext=tweets['camera'] .to_json() 
    zen = TextBlob(featext)
    feature = []
    for sentence in zen.sentences:
        sentx = get_sentiment(sentence.sentiment.polarity)
        feature.append(sentx)  
        
    total = len(zen.sentences)
    perc_pos = feature.count("positive") / total * 100
    perc_neg = feature.count("negative") / total * 100
    perc_neu = feature.count("neutral") / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for camera')
    plt.show()
    
    #sentiments analysis for animoji
    #same function as previous feature analytic
    featext=tweets['animoji'] .to_json() 
    zen = TextBlob(featext)
    feature = []
    for sentence in zen.sentences:
        sentx = get_sentiment(sentence.sentiment.polarity)
        feature.append(sentx)  
        
    total = len(zen.sentences)
    perc_pos = feature.count("positive") / total * 100
    perc_neg = feature.count("negative") / total * 100
    perc_neu = feature.count("neutral") / total * 100

    
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))
    labels = ['Neutral tweets', 'Positive tweets', 'Negative tweets']
    sizes = [perc_neu, perc_pos, perc_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('sentiments analysis for animoji')
    plt.show()
    
     
        
    
        
    
   
    