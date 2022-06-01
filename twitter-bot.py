import os
import logging
import tweepy
from time import sleep
from config import *

__author__ = 'Bryan Hohs'
__version__ = '2.0.0'
__maintainer__ = 'Bryan Hohs'
__email__ = 'bryan@hohs.us'
__status__ = 'Development'

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%r', level=logging.INFO)
logger = logging.getLogger()

def banner_text():
    logger.info("-------------------------------------------------")
    logger.info("                                                 ")
    logger.info(" _______ ________ _______ _______ ______ ___ ___ ")
    logger.info("|_     _|  |  |  |    ___|    ___|   __ \   |   |")
    logger.info("  |   | |  |  |  |    ___|    ___|    __/\     / ")
    logger.info("  |___| |________|_______|_______|___|    |___|  ")
    logger.info("            ______ _______ _______               ")
    logger.info("           |   __ \       |_     _|              ")
    logger.info("           |   __ <   -   | |   |                ")
    logger.info("           |______/_______| |___|                ")
    logger.info("                                                 ")
    logger.info("-------------------------------------------------")

def initialize_api():
    api = create_api()
    return api

def keywords():
    keywords = search_keywords
    scrub = urllib.parse.quote(keywords)
    return scrub

def get_tweets(api):
    tweets = tweepy.Cursor(api.search,
                    q=keywords() + " -filter:retweets",
                    count=number_of_tweets,
                    result_type=result_type,
                    monitor_rate_limit=True,
                    wait_on_rate_limit=True,
                    lang="en").items()
    return tweets

def process_tweets(api, tweets):
    for tweet in tweets:
        tweet = api.get_status(tweet.id)
        logger.info(f"🔎 Searching {result_type} tweets: {tweet.text[:20] + (tweet.text[20:] and '..')}")

        if tweet.user.id != api.me().id or tweet.in_reply_to_status_id is not None:

            if retweet_tweets:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        logger.info(f"👍 Tweet from @{tweet.user.screen_name}, retweeting now!")
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        raise e
                else:
                    logger.info(f"❌ Tweet from @{tweet.user.screen_name} has already been retweeted.")

            if like_tweets:
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                        logger.info(f"👍 Tweet from @{tweet.user.screen_name}, liking now!")
                        logger.info(f"⌛ Waiting {process_delay} seconds so we don't flood.")
                        sleep(process_delay)
                    except Exception as e:
                        logger.error("Error on favorite", exc_info=True)
                        raise e
                else:
                    logger.info(f"❌ Tweet from @{tweet.user.screen_name} has already been liked.")

        sleep(search_delay)

def exit_text():
    logger.info("Goodbye!")

if __name__ == "__main__":
    welcome = banner_text()
    api = initialize_api()
    tweets = get_tweets(api)
    process_tweets(api, tweets)

exit_text()
