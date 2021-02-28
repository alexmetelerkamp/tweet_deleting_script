# -*- coding: utf-8 -*-

""" Deletes all tweets below a certain retweet threshold.
    Forked from https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670
    https://twitter.com/chrisalbon
"""

import tweepy
from datetime import datetime

# Constants
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
USER_NAME = ''

# Connect To Your Twitter Account via Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))

# For the account name
def wipe(account_name=USER_NAME, favorite_threshold=100, days=62):
    # Get the current datetime
    current_date = datetime.utcnow()

    # For each tweet
    for status in tweepy.Cursor(api.user_timeline, screen_name='@'+account_name).items():
        # Get the tweet id
        status_id = status._json['id']

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Examining', status_id)

        # Get the number of favorites
        status_favorites = status._json['favorite_count']

        # Get the datetime of the tweet
        status_date = datetime.strptime(status._json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

        # Get whether you have favorited the tweet yourself
        status_favorited = status._json['favorited']

        # If the difference between the current datetime and the tweet's
        # is more than a day threshold
        if (datetime.utcnow() - status_date).days > days:
            # If the number of favorites is lower than the favorite threshold
            if status_favorites < favorite_threshold:
                # If you haven't favorited the tweet yourself
                if status_favorited == False:
                    # Delete the tweet
                    api.destroy_status(status_id)
                    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Deleting', status_id)

# Run main function
if __name__ == '__main__':
    wipe(account_name='AlexMetelerkamp', favorite_threshold=100, days=62)
