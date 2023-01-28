import pytest
from src import jikapibot


# check that like_tweets function is callable
def test_like_tweet_is_callable():
    assert callable(jikapibot.like_tweets)

# check that like_mentions function is callable
def test_like_mention_is_callable():
    assert callable(jikapibot.like_mentions)

# check that retweet_mentions function is callable
def test_retweet_tweet_is_callable():
    assert callable(jikapibot.retweet_mentions)
    

if __name__ == '__main__':
    pytest.main()
