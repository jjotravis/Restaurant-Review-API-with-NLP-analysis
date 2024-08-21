import mysql.connector
from mysql.connector import Error

class User:
    # Constants
    TYPE_REGULAR = "Regular"
    TYPE_ADMIN = "Admin"

    # Attributes
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = None
        self.zip_code = None
        self.birthday = None
        self.phone_number = None
        self.gender = None
        self.user_type = None

    def json_serialize(self):
        return {
            "userId": self.user_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "zipCode": self.zip_code,
            "birthday": self.birthday,
            "phoneNumber": self.phone_number,
            "gender": self.gender,
            "userType": self.user_type
        }

    def create(self, conn):
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO User (
                    userId, firstName, lastName, email, password, zipCode,
                    birthday, phoneNumber, gender, userType
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                self.user_id, self.first_name, self.last_name, self.email, 
                self.password, self.zip_code, self.birthday, self.phone_number, 
                self.gender, self.user_type
            )
            cursor.execute(query, values)
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
            conn.rollback()

    def update(self, conn):
        try:
            cursor = conn.cursor()
            query = """
                UPDATE User 
                SET firstName=%s, lastName=%s, email=%s, password=%s, zipCode=%s, 
                    birthday=%s, phoneNumber=%s, gender=%s, userType=%s 
                WHERE userId=%s
            """
            values = (
                self.first_name, self.last_name, self.email, self.password, 
                self.zip_code, self.birthday, self.phone_number, 
                self.gender, self.user_type, self.user_id
            )
            cursor.execute(query, values)
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
            conn.rollback()

    def load(self, conn):
        try:
            if not self.user_id:
                raise Exception("Error: user id is not set.")
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM User WHERE userId = %s"
            cursor.execute(query, (self.user_id,))
            user = cursor.fetchone()
            if user:
                self.first_name = user['firstName']
                self.last_name = user['lastName']
                self.email = user['email']
                self.password = user['password']
                self.zip_code = user['zipCode']
                self.birthday = user['birthday']
                self.phone_number = user['phoneNumber']
                self.gender = user['gender']
                self.user_type = user['userType']
            else:
                raise Exception(f"Error: user with id {self.user_id} does not exist.")
        except Error as e:
            print(f"Error: {e}")

    def delete(self, conn):
        try:
            if not self.user_id:
                raise Exception("Error: user id is not set.")
            cursor = conn.cursor()
            query = "DELETE FROM User WHERE userId = %s"
            cursor.execute(query, (self.user_id,))
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
            conn.rollback()

    @staticmethod
    def user_exists(conn, value, type='Id'):
        try:
            cursor = conn.cursor(dictionary=True)
            if type == 'Id':
                query = "SELECT * FROM User WHERE userId = %s"
                cursor.execute(query, (value,))
            elif type == 'Email':
                query = "SELECT * FROM User WHERE email = %s"
                cursor.execute(query, (value,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def user_email_used(conn, email, id):
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM User WHERE email = %s AND userId != %s"
            cursor.execute(query, (email, id))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def get_user_id_by_email(conn, email):
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT userId FROM User WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user['userId'] if user else None
        except Error as e:
            print(f"Error: {e}")
            return None
