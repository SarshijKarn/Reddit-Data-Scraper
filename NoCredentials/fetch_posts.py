import time
import logging
from datetime import datetime
from utils import make_request, safe_sleep

def fetch_posts(subreddit_name, start_year):
    """
    Fetch posts from subreddit JSON endpoint.
    """
    posts = []
    after = None
    
    # Create timestamp for Jan 1st of start_year
    cutoff_timestamp = int(time.mktime(time.strptime(f"01-01-{start_year}", "%d-%m-%Y")))
    
    logging.info(f"Fetching posts from r/{subreddit_name} (JSON)...")
    
    while True:
        url = f"https://www.reddit.com/r/{subreddit_name}/new.json"
        params = {'limit': 100}
        if after:
            params['after'] = after
            
        data = make_request(url, params)
        
        if not data or 'data' not in data or 'children' not in data['data']:
            logging.warning("No data returned or invalid format.")
            break
            
        children = data['data']['children']
        if not children:
            break
            
        for child in children:
            post_data = child['data']
            created_utc = post_data.get('created_utc', 0)
            
            if created_utc < cutoff_timestamp:
                logging.info(f"Reached posts from {datetime.fromtimestamp(created_utc).year}. Stopping.")
                return posts
                
            posts.append({
                "id": post_data.get('id'),
                "title": post_data.get('title'),
                "content": post_data.get('selftext', ''),
                "author": post_data.get('author', '[deleted]'),
                "created_utc": created_utc,
                "score": post_data.get('score', 0),
                "url": post_data.get('url', ''),
                "num_comments": post_data.get('num_comments', 0),
                "permalink": post_data.get('permalink')
            })
            
        after = data['data']['after']
        if not after:
            break
            
        logging.info(f"Fetched {len(posts)} posts so far...")
        safe_sleep(1, 2) # Be polite
        
    # Check limit warning
    if posts and posts[-1]["created_utc"] >= cutoff_timestamp:
         print(f"WARNING: r/{subreddit_name} has more than 1000 posts since {start_year}. Script will NOT fetch all of them due to Reddit limits.")
         logging.warning(f"r/{subreddit_name} has more than 1000 posts since {start_year}. Script will NOT fetch all of them due to Reddit limits.")
         
    return posts
