import redis

# Connect to the local Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

LEADERBOARD_KEY = "restaurant_leaderboard"

def add_or_update_restaurant_score(restaurant_id, score):
    """
    Add a restaurant to the leaderboard or update its score.
    The score should be the cumulative score calculated from the NLP sentiment analysis.
    """
    r.zincrby(LEADERBOARD_KEY, score, restaurant_id)
    print(f"Updated restaurant {restaurant_id} with score {score}.")


def get_top_restaurants(n=10):
    """
    Retrieve the top N restaurants from the leaderboard.
    """
    top_restaurants = r.zrevrange(LEADERBOARD_KEY, 0, n-1, withscores=True)
    return [(restaurant.decode('utf-8'), score) for restaurant, score in top_restaurants]


def get_restaurant_rank(restaurant_id):
    """
    Get the rank of a specific restaurant.
    """
    rank = r.zrevrank(LEADERBOARD_KEY, restaurant_id)
    if rank is not None:
        return rank + 1  # Rank is 0-based, so we add 1 for a human-readable rank
    else:
        return None


def remove_restaurant(restaurant_id):
    """
    Remove a restaurant from the leaderboard.
    """
    r.zrem(LEADERBOARD_KEY, restaurant_id)
    print(f"Removed restaurant {restaurant_id} from the leaderboard.")