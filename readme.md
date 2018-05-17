Simple python3 script to collect a specified number of tweets matching a keyword and store data in a csv file. Includes option to save only the tweets that have coordinates associated with them.

CSV file Headers:
- username, created_at, content, sentiment, polarity, retweet_status, place, lat, lon

*Requires tweepy, [textblob](http://textblob.readthedocs.io/en/dev/)
- pip3 install tweepy
- pip3 install textblob
- python3 main.py

*Twitter API keys are stored in apiconfig.py


```py
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
```