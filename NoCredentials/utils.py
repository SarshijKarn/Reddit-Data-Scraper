import os
import json
import time
import random
import logging
import requests

# -------------------------
# CONFIGURATION
# -------------------------
CHUNK_SIZE_MB = 100
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# -------------------------
# Logging setup
# -------------------------
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=LOG_FORMAT,
        filemode='a'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

# -------------------------
# Request Helpers
# -------------------------
def get_headers():
    """
    Return headers with a random user agent to avoid blocking.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return {
        'User-Agent': random.choice(user_agents)
    }

def safe_sleep(min_sec=2, max_sec=5):
    sleep_time = random.uniform(min_sec, max_sec)
    time.sleep(sleep_time)

def make_request(url, params=None):
    """
    Make a request with retry logic for 429s.
    """
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, headers=get_headers(), params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                logging.warning("Rate limited (429). Sleeping for 30 seconds...")
                time.sleep(30)
                continue
            else:
                logging.error(f"Request failed: {response.status_code} - {url}")
                return None
                
        except Exception as e:
            logging.error(f"Request exception: {e}")
            time.sleep(5)
            
    return None

# -------------------------
# JSON Helpers
# -------------------------
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def split_json_chunks(data, folder, base_name):
    os.makedirs(folder, exist_ok=True)
    filenames = []
    chunk = []
    chunk_index = 1
    approx_size = 0

    for item in data:
        item_size = len(json.dumps(item, ensure_ascii=False).encode('utf-8'))
        approx_size += item_size
        chunk.append(item)

        if approx_size >= CHUNK_SIZE_MB * 1024 * 1024:
            filename = os.path.join(folder, f"{base_name}_{chunk_index:03d}.json")
            save_json(chunk, filename)
            filenames.append(filename)
            chunk_index += 1
            chunk = []
            approx_size = 0

    if chunk:
        filename = os.path.join(folder, f"{base_name}_{chunk_index:03d}.json")
        save_json(chunk, filename)
        filenames.append(filename)

    return filenames
