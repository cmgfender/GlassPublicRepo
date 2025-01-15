"""
Twitter Brand Mention Scraper
-----------------------------
This script listens for new tweets that mention certain keywords (e.g., your brand
name). Once it finds them, it can store them in a CSV file or a database. You can
further expand it to trigger notifications (Slack, email, etc.).

Dependencies:
    pip install tweepy pandas

API Requirements:
    - You need a Twitter Developer account to get API keys and tokens.
    - https://developer.twitter.com/

Usage:
    1. Create a Twitter Developer account and set up a project/app.
    2. Replace the placeholders with your consumer_key, consumer_secret,
       access_token, and access_token_secret.
    3. Run the script in a Python environment.
"""

import tweepy
import pandas as pd
import datetime

# Twitter developer credentials (replace these with real values from your Twitter App)
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Keywords to track (add multiple if needed)
TRACKING_KEYWORDS = ["YourBrandName", "YourKeyword"]

# Authenticate to Twitter using Tweepy
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

def search_tweets(keyword, count=50):
    """
    Search recent tweets containing the specified keyword.
    
    Args:
        keyword (str): Keyword or brand name to search for on Twitter.
        count (int): Number of tweets to retrieve (limit according to your plan).
    
    Returns:
        list: A list of tweepy.Status objects containing the tweet data.
    """
    # Using Tweepy's search_tweets method to fetch the latest tweets containing 'keyword'
    try:
        tweets = api.search_tweets(q=keyword, count=count, lang="en", result_type="recent")
        return tweets
    except Exception as e:
        print(f"An error occurred while searching tweets: {e}")
        return []

def store_tweets_to_csv(tweets, filename="mentions.csv"):
    """
    Store tweet information in a CSV file.
    
    Args:
        tweets (list): A list of Tweepy status objects.
        filename (str): The filename for the output CSV.
        
    Returns:
        None
    """
    # Extract fields of interest from each tweet and store them in a list of dictionaries
    tweet_data = []
    for tweet in tweets:
        tweet_dict = {
            "tweet_id": tweet.id_str,
            "created_at": tweet.created_at,
            "user": tweet.user.screen_name,
            "text": tweet.text,
            "retweet_count": tweet.retweet_count,
            "favorite_count": tweet.favorite_count,
        }
        tweet_data.append(tweet_dict)

    # Convert list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(tweet_data)

    # Append to CSV if it exists; otherwise, create a new one
    try:
        existing_df = pd.read_csv(filename)
        combined_df = pd.concat([existing_df, df]).drop_duplicates(subset=["tweet_id"])
    except FileNotFoundError:
        combined_df = df

    combined_df.to_csv(filename, index=False)
    print(f"Stored {len(df)} new tweets in {filename}.")

def main():
    """
    Main function to iterate over all keywords and store tweets in CSV.
    """
    for keyword 
