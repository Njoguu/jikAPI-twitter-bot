from better_profanity import profanity
import os
import sys
import pytest
path = os.getcwd()
sys.path.append(path+"/src/")


# Test when tweet contains profanity
def test_has_profanity():
    tweet = "Oh, you piece of shit, @the_jikAPI"
    if not profanity.contains_profanity(tweet):
        prof = 0
    else:
        prof = 1
    assert prof == 1

# Test when tweet doesn't have profanity
def test_no_profanity():
    tweet = "Happy you"
    if not profanity.contains_profanity(tweet):
        prof = 0
    else:
        prof == 1
    assert prof == 0


if __name__ == '__main__':
    pytest.main()
