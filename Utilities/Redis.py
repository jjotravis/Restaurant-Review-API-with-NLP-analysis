import redis

class RedisClient:
    def __init__(self):
        self.client = redis.Redis()
        self.client.set_response_callback('error', lambda error: print(error))

    def is_alive(self):
        return self.client.ping()

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, duration):
        return self.client.setex(key, duration, value)

    def delete(self, key):
        return self.client.delete(key)

    def add_or_update_restaurant_score(self, restaurant_id, score):
        """
        Add a restaurant to the leaderboard or update its score.
        The score should be the cumulative score calculated from the NLP sentiment analysis.
        """
        self.client.zincrby(LEADERBOARD_KEY, score, restaurant_id)
        print(f"Updated restaurant {restaurant_id} with score {score}.")

    def get_top_restaurants(self, n=10):
        """
        Retrieve the top N restaurants from the leaderboard.
        """
        top_restaurants = self.client.zrevrange(LEADERBOARD_KEY, 0, n-1, withscores=True)
        return [(restaurant.decode('utf-8'), score) for restaurant, score in top_restaurants]

    def get_restaurant_rank(self, restaurant_id):
        """
        Get the rank of a specific restaurant.
        """
        rank = self.client.zrevrank(LEADERBOARD_KEY, restaurant_id)
        if rank is not None:
            return rank + 1  # Rank is 0-based, so we add 1 for a human-readable rank
        else:
            return None

    def remove_restaurant(self, restaurant_id):
        """
        Remove a restaurant from the leaderboard.
        """
        self.client.zrem(LEADERBOARD_KEY, restaurant_id)
        print(f"Removed restaurant {restaurant_id} from the leaderboard.")

    def __del__(self):
        del self.client

redis_client = RedisClient()
LEADERBOARD_KEY = "restaurant_leaderboard"