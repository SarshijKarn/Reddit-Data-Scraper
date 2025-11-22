# fetch_comments.py
import logging
from praw.models import MoreComments

def fetch_comments_for_post(reddit, post_id):
    """
    Fetch comments for a single post using PRAW.
    Returns list of comment dicts.
    """
    comments_list = []
    try:
        submission = reddit.submission(id=post_id)
        
        # This line expands the "MoreComments" objects. 
        # limit=0 removes all MoreComments (fetches everything), but can be slow.
        # limit=None fetches all.
        # For performance, we might want to set a threshold or leave some unexpanded.
        # Let's try to get a reasonable amount.
        submission.comments.replace_more(limit=None)
        
        def parse_comment(comment):
            if isinstance(comment, MoreComments):
                return None
                
            c_data = {
                "author": str(comment.author) if comment.author else "[deleted]",
                "content": comment.body,
                "created_utc": comment.created_utc,
                "score": comment.score,
                "replies": []
            }
            
            for reply in comment.replies:
                r = parse_comment(reply)
                if r:
                    c_data["replies"].append(r)
            return c_data

        for top_level_comment in submission.comments:
            parsed = parse_comment(top_level_comment)
            if parsed:
                comments_list.append(parsed)
                
    except Exception as e:
        logging.error(f"Error fetching comments for {post_id}: {e}")
        
    return comments_list

def fetch_comments_multithreaded(reddit, posts):
    """
    Fetch comments for all posts.
    Note: PRAW is not thread-safe if sharing the same session aggressively in complex ways,
    but read-only access is often fine. However, to be safe and simple, 
    we will iterate sequentially or use a simple loop. 
    Given the API limits and rate limits, sequential is safer to avoid 429s.
    """
    results = {}
    total = len(posts)
    
    for i, post in enumerate(posts):
        post_id = post["id"]
        if i % 10 == 0:
            logging.info(f"Fetching comments for post {i+1}/{total}...")
            
        comments = fetch_comments_for_post(reddit, post_id)
        results[post_id] = comments
        
    return results
