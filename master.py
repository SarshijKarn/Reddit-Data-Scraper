# master.py
import os
import json
import logging
import praw
from datetime import datetime
from fetch_posts import fetch_posts
from fetch_comments import fetch_comments_multithreaded
from clean_json import combine_posts_comments, save_chunks
from utils import setup_logging, safe_sleep, load_json, save_json

def main():
    # -----------------------------
    # User Inputs
    # -----------------------------
    print("--- Reddit Scraper (PRAW) ---")
    subreddit = input("Enter subreddit name (without r/): ").strip()
    start_year = int(input("Enter starting year (e.g., 2020): ").strip())
    
    print("\n--- API Credentials ---")
    print("If you have a praw.ini file, you can leave these blank.")
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    user_agent = input("User Agent (default: 'script:my_scraper:v1.0'): ").strip()
    
    if not user_agent:
        user_agent = "script:my_scraper:v1.0 (by /u/unknown)"

    # -----------------------------
    # Setup PRAW
    # -----------------------------
    if client_id and client_secret:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    else:
        # Fallback to praw.ini or env vars if empty
        reddit = praw.Reddit(user_agent=user_agent)

    # Verify credentials
    try:
        print(f"Logged in as: {reddit.user.me() or 'Read-only mode'}")
    except Exception as e:
        print(f"Warning: Authentication issue: {e}")
        print("Proceeding in read-only mode (if possible)...")

    output_folder = os.path.join(os.getcwd(), f"{subreddit}_data")
    os.makedirs(output_folder, exist_ok=True)

    log_file = os.path.join(output_folder, f"{subreddit}.log")
    setup_logging(log_file)

    # -----------------------------
    # Fetch posts
    # -----------------------------
    logging.info(f"Fetching posts from r/{subreddit} starting {start_year}...")
    posts = fetch_posts(reddit, subreddit, start_year)
    logging.info(f"Fetched {len(posts)} posts")

    if not posts:
        print("No posts found. Exiting.")
        return

    # -----------------------------
    # Fetch comments
    # -----------------------------
    logging.info("Fetching comments...")
    # Note: We renamed the function in fetch_comments.py but kept the import name for compatibility
    # logic inside fetch_comments_multithreaded was updated to be sequential/PRAW-safe
    comments_dict = fetch_comments_multithreaded(reddit, posts)
    logging.info("Comments fetching complete.")

    # -----------------------------
    # Combine posts + comments
    # -----------------------------
    combined = combine_posts_comments(posts, comments_dict)

    # -----------------------------
    # Save chunks + master JSON
    # -----------------------------
    master_file = save_chunks(combined, output_folder, subreddit)
    logging.info(f"Data saved. Master JSON: {master_file}")
    print(f"Done! Data saved to {output_folder}")

if __name__ == "__main__":
    main()
