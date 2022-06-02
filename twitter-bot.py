import os
import logging
import urllib.parse
import textwrap
import tweepy
from time import sleep
from config import *

__author__ = 'Bryan Hohs'
__version__ = '2.0.0'
__maintainer__ = 'Bryan Hohs'
__email__ = 'bryan@hohs.us'
__status__ = 'Development'

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%r', level=logging.INFO)
logger = logging.getLogger()

def banner_text():
    logger.info("------------------------------------------------------------")
    logger.info("                                                            ")
    logger.info("      _______ ________ _______ _______ ______ ___ ___       ")
    logger.info("     |_     _|  |  |  |    ___|    ___|   __ \   |   |      ")
    logger.info("       |   | |  |  |  |    ___|    ___|    __/\     /       ")
    logger.info("       |___| |________|_______|_______|___|    |___|        ")
    logger.info("                  ______ _______ _______                    ")
    logger.info("                 |   __ \       |_     _|                   ")
    logger.info("                 |   __ <   -   | |   |                     ")
    logger.info("                 |______/_______| |___|                     ")
    logger.info("                                                            ")
    logger.info("------------------------------------------------------------")

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
                    count=total_tweets,
                    result_type=result_type,
                    monitor_rate_limit=True,
                    wait_on_rate_limit=True,
                    lang="en").items()
    return tweets

def process_tweets(api, tweets):
    search_count = 0
    retweet_count = 0
    like_count = 0
    for tweet in tweets:
        tweet = api.get_status(tweet.id)
        search_count = search_count + 1
        tweet_text = textwrap.shorten(tweet.text, width=40, placeholder='...')
        logger.info(f"🔎 Searching {result_type} tweets for \"{search_keywords}\".")
        sleep(1)
        logger.info(f"🤖 @{tweet.user.screen_name}: {tweet_text}")

        if tweet.user.id != api.me().id or tweet.in_reply_to_status_id is not None:

            if retweet_tweets:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        retweet_count = retweet_count + 1
                        logger.info(f"😀 New tweet from @{tweet.user.screen_name}, retweeting now!")
                        sleep(1)
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        raise e
                else:
                    logger.info(f"😐 @{tweet.user.screen_name}'s tweet has already been retweeted.")
                    sleep(1)

            if like_tweets:
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                        like_count = like_count + 1
                        logger.info(f"😀 New like from @{tweet.user.screen_name}, liking now!")
                        logger.info(f"⌛ Sleeping {process_delay} seconds so we don't get banned.")
                        sleep(process_delay)
                    except Exception as e:
                        logger.error("Error on favorite", exc_info=True)
                        raise e
                else:
                    logger.info(f"😐 @{tweet.user.screen_name}'s tweet has already been liked.")
                    sleep(1)

        logger.info(f"🐦 tweets: [{search_count}/{total_tweets}] 🔁 retweets: [{retweet_count}/{total_tweets}] 👍 likes: [{like_count}/{total_tweets}]")
        sleep(search_delay)

def quit_message():
    quit_log = logger.info(f"✌️ Goodbye!")
    return quit_log

if __name__ == "__main__":
    welcome = banner_text()
    api = initialize_api()
    tweets = get_tweets(api)
    process_tweets(api, tweets)

quit_message()
