# clean_json.py
from utils import split_json_chunks, save_json
import os

def combine_posts_comments(posts, comments_dict):
    """
    Merge comments into post dicts
    Returns list of dicts ready for AI training
    """
    combined = []
    for post in posts:
        post_copy = post.copy()
        post_copy["comments"] = comments_dict.get(post["id"], [])
        combined.append(post_copy)
    return combined

def save_chunks(combined_data, output_folder, subreddit):
    """
    Split combined data into chunks (~100MB) and create master JSON referencing them
    """
    chunk_files = split_json_chunks(combined_data, output_folder, subreddit)
    master_json = {"subreddit": subreddit, "chunks": chunk_files}
    master_file = os.path.join(output_folder, f"{subreddit}_master.json")
    save_json(master_json, master_file)
    return master_file
