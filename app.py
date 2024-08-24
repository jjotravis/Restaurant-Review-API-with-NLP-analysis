from fastapi import FastAPI, HTTPException
from Models.Review import Review
from Utilities.db import DBClient
from Utilities.Redis import RedisClient
from spacytextblob.spacytextblob import SpacyTextBlob

app = FastAPI()

# Initialize DBClient and Redis handler
db = DBClient()
redis_handler = RedisClient()

# Load spaCy model
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

def analyze_sentiment(review_text):
    doc = nlp(review_text)
    polarity = doc._.blob.polarity
    return "positive" if polarity > 0 else "negative"

@app.post("/reviews")
async def submit_review(review: Review):
    sentiment = analyze_sentiment(review.review)
    score = 1 if sentiment == "positive" else -1

    # Insert review into MySQL DBClient
    db.execute_query(
        "INSERT INTO Reviews (restaurant_id, user_id, review_text, sentiment) VALUES (%s, %s, %s, %s)",
        (review.restaurant_id, review.user_id, review.review, sentiment)
    )

    # Update Redis leaderboard
    redis_handler.update_score(review.restaurant_id, score)

    return {"message": "Review submitted successfully", "sentiment": sentiment}

@app.get("/leaderboard")
async def get_leaderboard():
    leaderboard = redis_handler.get_leaderboard()
    return [{"restaurant_id": int(rest[0]), "score": int(rest[1])} for rest in leaderboard]

@app.get("/restaurants/{restaurant_id}/reviews")
async def get_reviews(restaurant_id: int):
    reviews = db.fetch_all("SELECT user_id, review_text, sentiment FROM Reviews WHERE restaurant_id = %s", (restaurant_id,))
    return [{"user_id": r[0], "review": r[1], "sentiment": r[2]} for r in reviews]

# Clean up on shutdown
@app.on_event("shutdown")
def shutdown_event():
    db.close()
