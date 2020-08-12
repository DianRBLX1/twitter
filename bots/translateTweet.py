#!/usr/bin/env python
# super-gt-bot/bots/translateTweet.py

import tweepy
import logging
from config import create_api
import six
from translate import Translator
import time

translator= Translator(to_lang="German")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_new_tweet(api, since_id):
    logger.info("Retrieving Tweets")
    new_since_id = since_id
    # superGT id = 2967005386
    for tweet in tweepy.Cursor(api.user_timeline, user_id=408575179, since_id=since_id, include_rts=False,
                               exclude_replies=True).items(1):
        text = tweet.text
        logger.critical(text)
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        result = translator.translate(text)

        new_since_id = max(tweet.id, new_since_id)
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)

        api.update_status(
            status=f"{result}\nhttps://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
        )

    logger.info('fetched')
    return new_since_id


def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_new_tweet(api, since_id)
        time.sleep(60)


if __name__ == "__main__":
    main()
