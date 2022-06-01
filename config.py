#
# tweepy bot forked from github
#
import tweepy
import logging
from credentials import *

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%r', level=logging.INFO)
logger = logging.getLogger()

# keywords to search for
search_keywords = "#bitcoin"

# time to wait between searching tweets in seconds 
search_delay = 15 

# time to wait before processing more tweets
process_delay = 180

# 'recent', 'popular', or 'mixed'
result_type = 'popular'

# number of tweets you want to fetch from twitter 
number_of_tweets = 60 

# like tweets 
like_tweets = True

# retweet tweets
retweet_tweets = True

def create_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error('Authentication Error', exc_info=True)
        raise e
    logger.info(f"Authentication OK. Connected to @{api.me().screen_name}")

    return api
