import os
import logging
from fetch_posts import fetch_posts
from fetch_comments import fetch_comments_sequential
from clean_json import combine_posts_comments, save_chunks
from utils import setup_logging

def main():
    # -----------------------------
    # User Inputs
    # -----------------------------
    print("--- Reddit Scraper (No Credentials) ---")
    print("WARNING: This method uses public JSON endpoints.")
    print("It is slower and less reliable than the API method.")
    print("-------------------------------------------")
    
    subreddit = input("Enter subreddit name (without r/): ").strip()
    start_year = int(input("Enter starting year (e.g., 2020): ").strip())
    
    output_folder = os.path.join(os.getcwd(), f"{subreddit}_data_noauth")
    os.makedirs(output_folder, exist_ok=True)

    log_file = os.path.join(output_folder, f"{subreddit}.log")
    setup_logging(log_file)

    # -----------------------------
    # Fetch posts
    # -----------------------------
    logging.info(f"Fetching posts from r/{subreddit} starting {start_year}...")
    posts = fetch_posts(subreddit, start_year)
    logging.info(f"Fetched {len(posts)} posts")

    if not posts:
        print("No posts found. Exiting.")
        return

    # -----------------------------
    # Fetch comments
    # -----------------------------
    logging.info("Fetching comments (this may take a while)...")
    comments_dict = fetch_comments_sequential(posts)
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
