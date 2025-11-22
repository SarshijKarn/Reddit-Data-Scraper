# utils.py
import os
import json
import time
import random
import logging

# -------------------------
# CONFIGURATION
# -------------------------
CHUNK_SIZE_MB = 100          # Split output JSON files every 100 MB

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
# Sleep randomly for safety
# -------------------------
def safe_sleep(min_sec=2, max_sec=5):
    sleep_time = random.uniform(min_sec, max_sec)
    time.sleep(sleep_time)

# -------------------------
# Save JSON to file
# -------------------------
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# -------------------------
# Load JSON from file
# -------------------------
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# -------------------------
# Split JSON into chunks
# -------------------------
def split_json_chunks(data, folder, base_name):
    """
    Splits a list of posts into multiple JSON files of approximately CHUNK_SIZE_MB
    Returns a list of filenames (to reference in master JSON)
    """
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

    # Save remaining
    if chunk:
        filename = os.path.join(folder, f"{base_name}_{chunk_index:03d}.json")
        save_json(chunk, filename)
        filenames.append(filename)

    return filenames
