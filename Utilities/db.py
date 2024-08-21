import mysql.connector
import os

class DBClient:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', 3306)
        self.database = os.getenv('DB_DATABASE', 'Hotel_Review')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'pass')
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def is_alive(self):
        return self.connection.is_connected()

    def nb_users(self):
        query = "SELECT COUNT(*) FROM users"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count

    def nb_restaurant(self):
        query = "SELECT COUNT(*) FROM restaurants"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count

db_client = DBClient()
