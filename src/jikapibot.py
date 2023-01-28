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
api = tweepy.API(auth)

# Limit Handler
def limit_handle(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.TooManyRequests:
        print("Limit reached, Sleeping!")
        time.sleep(8)
    except StopIteration:
            pass 

def like_mentions():
    # Find tweets that mention the account
    mentions = limit_handle(tweepy.Cursor(api.mentions_timeline).items())
    for mention in mentions:
        try:
            # like tweets that have been posted after 4 minutes
            time.sleep(240)
            api.create_favorite(mention.id)
            print(f"Liked tweet by {mention.user.screen_name}")
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def retweet_mentions():
    # Find tweets that mention the account
    mentions = limit_handle(tweepy.Cursor(api.mentions_timeline).items())
    for mention in mentions:
        try:
            # retweet tweets that have been posted after 4 minutes
            api.retweet(mention.id)
            print(f"Retweeted tweet by {mention.user.screen_name}")
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def like_tweets(tweet_hashtags): 
    # Check if the tweet contains any of the hashtags you are interested in
    for tweet in limit_handle(tweepy.Cursor(api.home_timeline).items(10)):    
        if any(hashtag in tweet.text for hashtag in tweet_hashtags):
            try:
                api.create_favorite(tweet.id)
                print(f"Liked tweet by {tweet.user.screen_name}")
            except tweepy.errors.Forbidden as err:
                if err.api_codes == 139:
                    print("Tweet already liked")
                else:
                    print(f"Error! {err}")

# Don't touch this 
def run_bot():
    print("*"*10 + "STARTING UP BOT" + "*"*10)
    print("*"*10 + "LISTENING..." + "*"*10)
    while True:
        like_mentions()
        retweet_mentions()
        like_tweets(tweet_hashtags)

if __name__ == '__main__':
    tweet_hashtags = ["#jobs", "#ikokazike", "#jobsearch", "#hiring", "#JobOpportunitiesKE",
        "#HiringKE","#CareerOpportunitiesKE","#JobsinKenya", "#KenyanJobs", "#EmploymentKE",
        "#WorkinKenya","#CareerKE","#JobVacanciesKE", "#KenyaEmployment"
    ]
    run_bot()
