# fetch_posts.py
import time
import logging
from datetime import datetime

def fetch_posts(reddit, subreddit_name, start_year):
    """
    Fetch posts from subreddit starting from start_year using PRAW.
    Returns a list of post dicts with metadata.
    Note: Reddit API limits listing to ~1000 items.
    """
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    # Create timestamp for Jan 1st of start_year
    cutoff_timestamp = int(time.mktime(time.strptime(f"01-01-{start_year}", "%d-%m-%Y")))
    
    logging.info(f"Fetching posts from r/{subreddit_name} via PRAW (Newest first)...")
    
    try:
        # Fetch new posts. Limit=None fetches as many as possible (approx 1000)
        for submission in subreddit.new(limit=None):
            if submission.created_utc < cutoff_timestamp:
                logging.info(f"Reached posts from {datetime.fromtimestamp(submission.created_utc).year}. Stopping.")
                break
            
            posts.append({
                "id": submission.id,
                "title": submission.title,
                "content": submission.selftext,
                "author": str(submission.author) if submission.author else "[deleted]",
                "created_utc": submission.created_utc,
                "score": submission.score,
                "url": submission.url,
                "num_comments": submission.num_comments
            })
            
            if len(posts) % 100 == 0:
                logging.info(f"Fetched {len(posts)} posts so far...")
                
    except Exception as e:
        logging.error(f"Error fetching posts: {e}")

    # Check if we reached the start year
    if posts and posts[-1]["created_utc"] >= cutoff_timestamp:
         print(f"WARNING: r/{subreddit_name} has more than 1000 posts since {start_year}. Script will NOT fetch all of them due to Reddit API limits.")
         logging.warning(f"r/{subreddit_name} has more than 1000 posts since {start_year}. Script will NOT fetch all of them due to Reddit API limits.")

    return posts
