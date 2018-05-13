import re
import json
import tweepy
import csv
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
#from textblob import TextBlob
from apiconfig import *

#Collects tweets with selected keyword & outputs basic info to csv file

def main():

    #Set up twitter api auth
    auth = OAuthHandler(comsumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    #Select the file name, topic, and # of tweets to collect
    filename = input("Enter a filename: ")
    searchterm = input("Enter a search term: ")
    tweetcount = input("Enter the target number of tweets: ")

    #Set up listener
    class TweepyListener(tweepy.StreamListener):
        counter = 0
        print("Searching for " + tweetcount + " tweets on the topic \'" + searchterm + "\'")

        def on_status(self, status):
            #print(status.text)
            print('')

        def on_error(self, status_code):
            if status_code == 420:
                # returning False in on_data disconnects the stream
                return False
        #Opens a csv file and writes to a new line:
        #Time/date and tweet text of each tweet sent.
        #Include coordinates if available.
        def on_data(self, raw_data):
            if TweepyListener.counter < int(tweetcount):
                json_data = json.loads(raw_data)
                content = json_data['text']
                created = json_data['created_at']
                print(content)
                coords = json_data["coordinates"]
                with open('%s.csv' % filename, 'a', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([created,content,coords])
                TweepyListener.counter += 1
            else:
                print('done! *-* \nSaved ' + str(TweepyListener.counter) + ' tweets to ' + '%s.csv' % filename)
                return False

    tweepyListener = TweepyListener()
    myStream = tweepy.Stream(auth=api.auth, listener=TweepyListener())
    myStream.filter(track=[searchterm],async=True)

    print('processing *~*')

if __name__ == "__main__":
    # calling main function
    main()