import pytest
import sys
import os
path = os.getcwd()
sys.path.append(path+"/src/")
from jikapibot import like_mentions, like_tweets, retweet_mentions


# check that like_tweets function is callable
def test_like_tweet_is_callable():
    assert callable(like_tweets)

# check that like_mentions function is callable
def test_like_mention_is_callable():
    assert callable(like_mentions)

# check that retweet_mentions function is callable
def test_retweet_tweet_is_callable():
    assert callable(retweet_mentions)
    

if __name__ == '__main__':
    pytest.main()
