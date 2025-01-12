import praw
import os
def fetch_reddit_data(topic):
    # Setup Reddit API client
    reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'), 
                         client_secret=os.getenv('REDDIT_CLIENT_SECRET'), 
                         user_agent=os.getenv('REDDIT_USER_AGENT'))
    
    # Fetch posts from Reddit for the topic
    posts = []
    for submission in reddit.subreddit('all').search(topic, limit=5):
        posts.append({
            "title": submission.title,
            "content": submission.selftext,
            "url": submission.url
        })
    
    return posts
