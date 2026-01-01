# Reddit Data Scraper (Year Wise)

A powerful Python tool to scrape posts and comments from a specific subreddit starting from a given year.

This project offers two ways to scrape data:
1.  **With API Credentials (Recommended)**: Faster, more reliable, uses the official Reddit API (PRAW).
2.  **No Credentials**: Works out-of-the-box without API keys, but is slower and relies on public JSON pages.

## ⚠️ Important Limitation
**Reddit API Limit**: Both methods are restricted by Reddit to fetch only the **last ~1000 posts** from a subreddit.
-   If the subreddit is small, you might get the full year's data.
-   If the subreddit is active, you will only get the most recent posts (e.g., last few weeks/months).

---

## Option 1: With API Credentials (Recommended)
Use this method for better stability and speed.

### Setup
1.  **Get Credentials**:
    -   Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
    -   Create a "script" app.
    -   Note your **Client ID** (under the name) and **Client Secret**.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1.  Run the script:
    ```bash
    python master.py
    ```
2.  Enter the Subreddit name and Start Year.
3.  Enter your Client ID and Client Secret when prompted.

---

## Option 2: No Credentials (Easiest)
Use this method if you don't want to set up an API account.

### Setup
1.  Navigate to the `NoCredentials` folder:
    ```bash
    cd NoCredentials
    ```
2.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1.  Run the script:
    ```bash
    python master.py
    ```
2.  Enter the Subreddit name and Start Year.

*Note: This method includes artificial delays to avoid getting blocked by Reddit, so it will be slower.*

---

## Output
The script creates a folder named `{subreddit}_data` (or `{subreddit}_data_noauth`) containing:
-   `{subreddit}_master.json`: The main file containing all posts and comments.
-   `{subreddit}_001.json`: Data chunks (if the data is large).
-   `{subreddit}.log`: Log file of the scraping process.

### Data Structure
```json
[
  {
    "id": "post_id",
    "title": "Post Title",
    "content": "Post content...",
    "author": "username",
    "created_utc": 1609459200,
    "comments": [
      {
        "author": "commenter",
        "content": "Comment body...",
        "replies": [...]
      }
    ]
  }
]
```

---

## 🙏 Credits
Built with:

*   **Python** - Programming language
*   **PRAW** - Python Reddit API Wrapper
*   **Requests** - HTTP library for No-Auth version
*   **JSON** - Data storage format

## 📊 Stats
![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-~500-blue)
![Files](https://img.shields.io/badge/Files-10-green)
![Features](https://img.shields.io/badge/Features-Scraping%2C%20No--Auth-orange)

---
<div align="center">

### Created with ❤️ by Sarshij Karn

[![Website](https://img.shields.io/badge/Website-sarshijkarn.com.np-8a2be2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://sarshijkarn.com.np)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sarshij-karn-1a7766236/)

</div>
