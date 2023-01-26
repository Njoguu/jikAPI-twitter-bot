import tweepy
import time
from os import environ
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file
INTERVAL = 60 * 60 # --> Check mentions every hour

# Twitter API keys
api_key = environ['API_KEY']
api_key_secret = environ['API_KEY_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def like_mentions():
    # Find tweets that mention the account
    mentions = api.mentions_timeline()
    for mention in mentions:
        try:
            # like tweets that have been posted after 4 minutes
            time.sleep(240)
            api.create_favorite(mention.id)
            print(f"Liked tweet by {mention.user.screen_name}")
            time.sleep(INTERVAL)
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def retweet_mentions():
    # Find tweets that mention the account
    mentions = api.mentions_timeline()
    for mention in mentions:
        try:
            # retweet tweets that have been posted after 4 minutes
            time.sleep(240)
            api.retweet(mention.id)
            print(f"Retweeted tweet by {mention.user.screen_name}")
            time.sleep(INTERVAL)
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def like_tweets():
    # TODO --> Find and like Tweets with certain keywords
    pass

# Don't touch this 
def run_bot():
    print("*"*10 + "STARTING UP BOT" + "*"*10)
    print("*"*10 + "LISTENING..." + "*"*10)
    while True:
        like_mentions()
        retweet_mentions()

if __name__ == '__main__':
    run_bot()