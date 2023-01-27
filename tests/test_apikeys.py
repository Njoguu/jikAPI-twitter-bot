import tweepy
import pytest
import os
from dotenv import load_dotenv

load_dotenv()


def test_api_keys():

    # Get API keys from .env
    api_key = os.getenv('API_KEY')
    api_key_secret = os.getenv('API_KEY_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    assert isinstance(api_key, str)
    assert isinstance(api_key_secret, str)
    assert isinstance(access_token, str)
    assert isinstance(access_token_secret, str)

    auth = tweepy.OAuth1UserHandler(
        api_key,
        api_key_secret,
        access_token,
        access_token_secret,
    )

    api = tweepy.API(auth)

    assert api.verify_credentials()


if __name__ == "__main__":
    pytest.main()