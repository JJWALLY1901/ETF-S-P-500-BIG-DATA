import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

def get_twitter_data():
    """Recolecta tweets con hashtag #SP500"""
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    client = tweepy.Client(bearer_token=bearer_token)
    
    query = '#SP500 lang:es -is:retweet'
    
    try:
        tweets = client.search_recent_tweets(
            query=query,
            tweet_fields=['created_at', 'author_id', 'public_metrics'],
            max_results=50
        )
        
        data = [{
            'id': tweet.id,
            'text': tweet.text,
            'author_id': tweet.author_id,
            'created_at': str(tweet.created_at),
            'retweets': tweet.public_metrics['retweet_count'],
            'likes': tweet.public_metrics['like_count']
        } for tweet in tweets.data]
        
        # Guardar datos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../data/twitter_sp500_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Se guardaron {len(data)} tweets en {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al obtener tweets: {str(e)}")
        return None

if __name__ == "__main__":
    get_twitter_data()