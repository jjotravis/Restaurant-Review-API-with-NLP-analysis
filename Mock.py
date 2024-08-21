from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import mysql.connector
from textblob import TextBlob

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="Hotel_Review"
)
cursor = conn.cursor()

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()

class Review(BaseModel):
    restaurant_id: int
    user_id: int
    review: str

def analyze_sentiment(review_text):
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity
    return "positive" if polarity > 0 else "negative"

@app.post("/reviews")
async def submit_review(review: Review):
    sentiment = analyze_sentiment(review.review)

    # Insert review into MySQL database
    cursor.execute(
        "INSERT INTO Reviews (restaurant_id, user_id, review_text, sentiment) VALUES (%s, %s, %s, %s)",
        (review.restaurant_id, review.user_id, review.review, sentiment)
    )
    conn.commit()

    # Update Redis leaderboard
    score = 1 if sentiment == "positive" else -1
    r.zincrby("restaurant_leaderboard", score, review.restaurant_id)

    return {"message": "Review submitted successfully", "sentiment": sentiment}

@app.get("/leaderboard")
async def get_leaderboard():
    leaderboard = r.zrevrange("restaurant_leaderboard", 0, 9, withscores=True)
    return [{"restaurant_id": int(rest[0]), "score": int(rest[1])} for rest in leaderboard]

@app.get("/restaurants/{restaurant_id}/reviews")
async def get_reviews(restaurant_id: int):
    cursor.execute("SELECT user_id, review_text, sentiment FROM Reviews WHERE restaurant_id = %s", (restaurant_id,))
    reviews = cursor.fetchall()
    return [{"user_id": r[0], "review": r[1], "sentiment": r[2]} for r in reviews]

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
