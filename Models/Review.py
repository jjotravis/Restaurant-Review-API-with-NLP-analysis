import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel

class Review(BaseModel):
    def __init__(self):
        self.review_id = None
        self.restaurant_id = None
        self.user_id = None
        self.review_text = None
        self.sentiment = None
        self.timestamp = None

    def json_serialize(self):
        return {
            "review_id": self.review_id,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id,
            "review_text": self.review_text,
            "sentiment": self.sentiment,
            "timestamp": self.timestamp
        }

    def create(self, db_connection):
        try:
            cursor = db_connection.cursor()
            sql = """
            INSERT INTO Review (reviewId, restaurantId, userId, reviewText, sentiment, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (self.review_id, self.restaurant_id, self.user_id, self.review_text, self.sentiment, self.timestamp)
            cursor.execute(sql, values)
            db_connection.commit()
        except Error as e:
            print(f"Error: {e}")
            db_connection.rollback()
        finally:
            cursor.close()

    def update(self, db_connection):
        try:
            cursor = db_connection.cursor()
            sql = """
            UPDATE Review 
            SET restaurantId=%s, userId=%s, reviewText=%s, sentiment=%s, timestamp=%s
            WHERE reviewId=%s
            """
            values = (self.restaurant_id, self.user_id, self.review_text, self.sentiment, self.timestamp, self.review_id)
            cursor.execute(sql, values)
            db_connection.commit()
        except Error as e:
            print(f"Error: {e}")
            db_connection.rollback()
        finally:
            cursor.close()

    def load(self, db_connection):
        try:
            if not self.review_id:
                raise ValueError("Error: review id is not set.")

            cursor = db_connection.cursor(dictionary=True)
            sql = "SELECT * FROM Review WHERE reviewId = %s"
            cursor.execute(sql, (self.review_id,))
            record = cursor.fetchone()

            if record:
                self.restaurant_id = record['restaurantId']
                self.user_id = record['userId']
                self.review_text = record['reviewText']
                self.sentiment = record['sentiment']
                self.timestamp = record['timestamp']
            else:
                raise ValueError(f"Error: this review with id {self.review_id} does not exist in the database.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def delete(self, db_connection):
        try:
            if not self.review_id:
                raise ValueError("Error: review id is not set.")

            cursor = db_connection.cursor()
            sql = "DELETE FROM Review WHERE reviewId = %s"
            cursor.execute(sql, (self.review_id,))
            db_connection.commit()
        except Error as e:
            print(f"Error: {e}")
            db_connection.rollback()
        finally:
            cursor.close()

    @staticmethod
    def review_exists(db_connection, review_id):
        try:
            cursor = db_connection.cursor(dictionary=True)
            sql = "SELECT * FROM Review WHERE reviewId = %s"
            cursor.execute(sql, (review_id,))
            record = cursor.fetchone()
            return record is not None
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
