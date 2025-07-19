import praw
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_reddit_client():
    return praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )

def scrape_reddit(subreddit='investing', limit=50):
    try:
        reddit = get_reddit_client()
        sub = reddit.subreddit(subreddit)
        
        posts = []
        for post in sub.hot(limit=limit):
            posts.append({
                'id': post.id,
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'comments': post.num_comments,
                'created_utc': post.created_utc,
                'url': post.url,
                'selftext': post.selftext
            })
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('../data/reddit', exist_ok=True)
        
        filename = f'../data/reddit/{subreddit}_posts_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=4)
            
        print(f"Se guardaron {len(posts)} posts en {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al obtener posts de Reddit: {str(e)}")
        return None

if __name__ == "__main__":
    scrape_reddit()