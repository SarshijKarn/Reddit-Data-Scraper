import logging
from utils import make_request, safe_sleep

def fetch_comments_for_post(post_id, permalink):
    """
    Fetch comments for a single post using JSON endpoint.
    """
    url = f"https://www.reddit.com{permalink}.json"
    data = make_request(url)
    
    comments_list = []
    
    if not data or len(data) < 2:
        return comments_list
        
    # data[0] is the post, data[1] is the comments
    comments_data = data[1]['data']['children']
    
    def parse_comment(comment_dict):
        if comment_dict['kind'] == 'more':
            return None
            
        c_data = comment_dict['data']
        parsed = {
            "author": c_data.get('author', '[deleted]'),
            "content": c_data.get('body', ''),
            "created_utc": c_data.get('created_utc', 0),
            "score": c_data.get('score', 0),
            "replies": []
        }
        
        if 'replies' in c_data and c_data['replies']:
            replies_data = c_data['replies']['data']['children']
            for reply in replies_data:
                r = parse_comment(reply)
                if r:
                    parsed["replies"].append(r)
                    
        return parsed

    for comment in comments_data:
        parsed = parse_comment(comment)
        if parsed:
            comments_list.append(parsed)
            
    return comments_list

def fetch_comments_sequential(posts):
    """
    Fetch comments for all posts sequentially.
    """
    results = {}
    total = len(posts)
    
    for i, post in enumerate(posts):
        post_id = post["id"]
        permalink = post.get("permalink")
        
        if not permalink:
            continue
            
        if i % 5 == 0:
            logging.info(f"Fetching comments for post {i+1}/{total}...")
            
        comments = fetch_comments_for_post(post_id, permalink)
        results[post_id] = comments
        
        # Sleep to avoid rate limits
        safe_sleep(1.5, 3)
        
    return results
