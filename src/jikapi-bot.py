import tweepy
import time, os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file

# Twitter API keys
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def like_mentions():
    # Find tweets that mention the account
    mentions = api.mentions_timeline()
    for mention in mentions:
        try:
            # Only like tweets that have been posted after 2 minutes 
            time.sleep(120)
            api.create_favorite(mention.id)
            print(f"Liked tweet by {mention.user.screen_name}")
        except Exception as err:
            print(f"Error! {err}")

def retweet_mentions():
    # Find tweets that mention the account
    mentions = api.mentions_timeline()
    for mention in mentions:
        try:
            # Only retweet tweets that have been posted after 2 minutes 
            time.sleep(120)
            api.retweet(mention.id)
            print(f"Retweeted tweet by {mention.user.screen_name}")
        except Exception as err:
            print(f"Error! {err}")

def like_tweets():
    # TODO --> Find and like Tweets with certain keywords
    pass

# Don't touch this 
def run_bot():
    while True:
        like_mentions()
        retweet_mentions()

if __name__ == '__main__':
    run_bot()