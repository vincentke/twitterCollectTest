import re
import json
import tweepy
import csv
import os
from textblob import TextBlob
from apiconfig import *

#Collects tweets with selected keyword & outputs basic info to csv file
def main():

    #Set up twitter api auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    #Select the file name, topic, and # of tweets to collect
    filename_raw = input("Enter a filename: ")
    filename = ''.join(i for i in filename_raw if i not in '<>:"/\|?*')

    if not os.path.exists('%s.csv' % filename):
        with open('%s.csv' % filename, 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'created_at', 'content', 'sentiment', 'polarity',
                             'retweet_status','place','lat', 'lon'])
    searchterm = input("Enter a search term: ")
    while True:
        try:
            tweetcount = int(input("Enter the target number of tweets: "))
        except ValueError:
            print("Not an integer")
        else:
            break

    geotagged = input("Only save tweets with coordinates? y/n: ").lower()
    while(geotagged not in ['y', 'n', 'yes', 'no']):
        geotagged = input("Please choose y/n: ")
    needCoords = False
    if geotagged == 'y' or geotagged == 'yes':
        needCoords = True

    #Set up listener
    class TweepyListener(tweepy.StreamListener):
        counter = 0
        print("Searching for " + str(tweetcount) + " tweets on the topic \'" + searchterm + "\'")

        def on_status(self, status):
            #print(status.text)
            print('')

        #Rate limit error
        def on_error(self, status_code):
            if status_code == 420:
                # returning False in on_data disconnects the stream
                return False
        #Opens a csv file and writes to a new line:
        #Screen name, time/date, tweet text, and sentiment analysis of each tweet sent.
        #Include location and coordinates if available.
        def on_data(self, raw_data):
            if TweepyListener.counter < int(tweetcount):

                #loading data
                json_data = json.loads(raw_data)
                coords = None
                place = None
                raw_content = 'n/a'
                content = 'n/a'
                created = 'n/a'
                retweet = False
                username = 'n/a'
                sentiment = 'n/a'
                polarity = 0.0

                if 'user' in json_data:
                    username = json_data['user']['screen_name']

                if 'text' in json_data:
                    raw_content = json_data['text']
                if 'extended_tweet' in json_data:
                    extended = json_data['extended_tweet']
                    raw_content = extended['full_text']

                if 'retweeted_status' in json_data:
                    retweet_data = json_data['retweeted_status']
                    retweet = True
                    raw_content = retweet_data['text']
                if 'created_at' in json_data:
                    created = json_data['created_at']

                if 'coordinates' in json_data:
                    coords = json_data['coordinates']
                if 'place' in json_data:
                    place_data = json_data['place']
                    if place_data is not None and 'full_name' in place_data:
                        place = place_data['full_name']

                content = str(raw_content).replace('\n', ' ').replace('\r', ' ')
                analysis = TextBlob(content).sentiment
                polarity = '%.1f' % round(analysis.polarity * 100.00, 1) + '%'
                if analysis.polarity > 0:
                    sentiment = 'positive'
                elif analysis.polarity < 0:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'

                #printing tweets and writing to file
                if  not needCoords or needCoords and coords is not None:
                    print('-----------------*' + str(TweepyListener.counter + 1) + '*-----------------')
                    print(raw_content)
                    print(username + ' ' + created)
                    with open('%s.csv' % filename, 'a', encoding='utf-8-sig', newline='') as file:
                        writer = csv.writer(file)
                        #extract the latitude and longitude from the coordinates field
                        if coords is not None:
                            lat = coords['coordinates'][1]
                            lon = coords['coordinates'][0]
                            writer.writerow([username,created,content,sentiment,polarity,retweet,place,lat,lon])
                        else:
                            writer.writerow([username,created,content,sentiment,polarity,retweet,place])
                    TweepyListener.counter += 1
            else:
                print('done! *-* \nSaved ' + str(TweepyListener.counter) + ' tweets to ' + '%s.csv' % filename)
                return False

    tweepyListener = TweepyListener()
    myStream = tweepy.Stream(auth=api.auth, listener=TweepyListener(), tweet_mode='extended')
    myStream.filter(track=[searchterm],async=True)

    print('processing *~*')

if __name__ == "__main__":
    # calling main function
    main()