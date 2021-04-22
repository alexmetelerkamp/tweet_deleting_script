# -*- coding: utf-8 -*-
""" Deletes all tweets below a certain retweet threshold.
    Forked from https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670
    Thanks to https://twitter.com/chrisalbon
"""

import os
import tweepy
from datetime import datetime

# Constants - these are stored in Replit Secrets
# Get these from Twitter API 
CONSUMER_KEY = os.getenv("ENV_API_KEY")
CONSUMER_SECRET = os.getenv("ENV_API_SECRET")

# Username without "@"
USER_NAME = os.getenv('ENV_TWITTER_USERNAME')

# Get these from Twitter Dev Dashboard
ACCESS_TOKEN = os.getenv('ENV_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ENV_ACCESS_SECRET')

# Connect To Your Twitter Account via Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# Token and secret copied manually from Twitter Dev Dashboard
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))


def wipe(account_name=USER_NAME, favorite_threshold=1, days=1000):
  # Get the current datetime
  current_date = datetime.utcnow()

  # To track deletions
  count = 0

  # For each tweet
  for status in tweepy.Cursor(api.user_timeline,screen_name='@' + account_name).items():

    # Get the tweet id
    status_id = status._json['id']

    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Examining', status_id)

    # Get the number of favorites
    status_favorites = status._json['favorite_count']

    # Get the datetime of the tweet
    status_date = datetime.strptime(status._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

    # Get whether you have favorited the tweet yourself
    status_favorited = status._json['favorited']

    # If the difference between the current datetime and the tweet's is more than a day threshold
    if (datetime.utcnow() - status_date).days > days:
      # If the number of favorites is lower than the favorite threshold
      if status_favorites < favorite_threshold:
        # If you haven't favorited the tweet yourself
        if status_favorited == False:
          
          # info of deleted tweet and total progress
          print(status_date)
          print(status._json['text'])
          print(count, ' tweets found')

          # Delete the tweet
          #api.destroy_status(status_id)
          count += 1

#Borrowed from https://gist.github.com/shollingsworth
def yesno(question):
    """Simple Yes/No Function."""
    prompt = f'{question} ? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False


# Run main function
if __name__ == '__main__':

  #Confirm execution
  ans = yesno("Are you sure you want to run the script? (Incorrect config could wipe ALL tweets)")
  print(f'Your answer was: {ans}')
  
  # Run wipe on confirmation
  if ans:
    wipe(account_name=USER_NAME, favorite_threshold=1, days=7)
  else:
    print('OK phew. Disaster avoided')
