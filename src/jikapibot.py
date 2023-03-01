import time
import json
import openai
import tweepy
import requests
from os import environ
from dotenv import load_dotenv
from better_profanity import profanity

load_dotenv()  # take environment variables from .env file

# Twitter API keys
api_key = environ['API_KEY']
api_key_secret = environ['API_KEY_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# OpenAI API setup
openai.organization = environ["OPENAI_ORGANIZATION"]
openai.api_key = environ["OPENAI_API_KEY"]


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
            if not profanity.contains_profanity(mention.text):
                api.create_favorite(mention.id)
                print(f"Liked tweet by {mention.user.screen_name}")
            else: 
                print(f"Tweet contains profanity! Did not like tweet!")
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def retweet_mentions():
    # Find tweets that mention the account
    mentions = limit_handle(tweepy.Cursor(api.mentions_timeline).items())
    for mention in mentions:
        try:
            # retweet tweets that have been posted after 4 minutes
            if not profanity.contains_profanity(mention.text):
                api.retweet(mention.id)
                print(f"Retweeted tweet by {mention.user.screen_name}")
            else:
                print(f"Tweet contains profanity! Did not retweet mention!")
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

def like_tweets(tweet_hashtags): 
    # Check if the tweet contains any of the hashtags you are interested in
    for tweet in limit_handle(tweepy.Cursor(api.home_timeline).items(10)):    
        if any(hashtag in tweet.text for hashtag in tweet_hashtags):
            try:
                if not profanity.contains_profanity(tweet.text):
                    api.create_favorite(tweet.id)
                    print(f"Liked tweet by {tweet.user.screen_name}")
                else:
                    print(f"Tweet contains profanity! Did not like tweet!")
            except tweepy.errors.Forbidden as err:
                if err.api_codes == 139:
                    print("Tweet already liked")
                else:
                    print(f"Error! {err}")

def tweet_commit_messages():
    owner = 'Njoguu'
    repo = 'jikAPI'

    # Post the commit message
    try: 
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'

        # make the API request
        response = requests.get(url)
        data = json.loads(response.text)[0]
        message = data['commit']['message']

        # Get the latest tweet
        tweets = api.user_timeline(count=1)

        # Check if the tweet already exists
        for tweet in tweets:
            if tweet.text == message:
                # Wait until a new message is available
                break
        else:
            # Tweet the message
            api.update_status(status=message) 
            print(f"Tweeted: {message}")
    except Exception as err:
        print(err)

def reply_to_messages():
    # get the tweet to reply to
    tweets = api.mentions_timeline(count=1)
    for tweet in tweets:
        try:
            if not profanity.contains_profanity(tweet.text):
                # use openai's API to reply to the tweet 
                prompt = f"Reply to this tweet: {tweet.text}"
                req = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.3,
                    max_tokens=1024,
                    n=1,
                    stop=None
                )
                response = req.get('choices')[0]['text'].strip()

                # Post the generated reply as a reply to the original tweet
                api.update_status(
                    status=response,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
                print(f"Replied to tweet by {tweet.user.screen_name}")
            else:
                print(f"Tweet contains profanity! Did not reply to mention!")
        except tweepy.TweepyException as e:
            print(f"Error! {e}")

# Don't touch this 
def run_bot():
    print("*"*10 + "STARTING UP BOT" + "*"*10)
    print("*"*10 + "LISTENING..." + "*"*10)
    while True:
        like_mentions()
        retweet_mentions()
        like_tweets(tweet_hashtags)
        tweet_commit_messages()
        # reply_to_messages()
       

if __name__ == '__main__':
    tweet_hashtags = ["#jobs", "#ikokazike", "#jobsearch", "#hiring", "#JobOpportunitiesKE",
        "#HiringKE","#CareerOpportunitiesKE","#JobsinKenya", "#KenyanJobs", "#EmploymentKE",
        "#WorkinKenya","#CareerKE","#JobVacanciesKE", "#KenyaEmployment"
    ]
    run_bot()
