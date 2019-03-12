import os
from dotenv import load_dotenv
import tweepy


load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# api = Twitter(auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
