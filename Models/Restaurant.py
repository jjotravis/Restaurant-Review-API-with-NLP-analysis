import mysql.connector
from mysql.connector import Error
import json

class Restaurant:
    def __init__(self, restaurant_id=None, name=None, phone_number=None, address=None, second_address=None, 
                 city=None, state=None, zip_code=None, website=None, user_id=None):
        self.restaurant_id = restaurant_id
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.second_address = second_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.website = website
        self.user_id = user_id

    def json_serialize(self):
        return {
            "restaurantId": self.restaurant_id,
            "name": self.name,
            "phoneNumber": self.phone_number,
            "address": self.address,
            "secondAddress": self.second_address,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zip_code,
            "website": self.website,
            "userId": self.user_id
        }

    def create(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor()
                insert_query = """INSERT INTO Restaurant (restaurantId, name, phoneNumber, address, secondAddress, city, state, zipCode, website, userId) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                record = (self.restaurant_id, self.name, self.phone_number, self.address, self.second_address, self.city, self.state, self.zip_code, self.website, self.user_id)
                cursor.execute(insert_query, record)
                connection.commit()

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor()
                update_query = """UPDATE Restaurant SET name=%s, phoneNumber=%s, address=%s, secondAddress=%s, city=%s, state=%s, zipCode=%s, website=%s, userId=%s 
                                  WHERE restaurantId=%s"""
                record = (self.name, self.phone_number, self.address, self.second_address, self.city, self.state, self.zip_code, self.website, self.user_id, self.restaurant_id)
                cursor.execute(update_query, record)
                connection.commit()

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                load_query = "SELECT * FROM Restaurant WHERE restaurantId = %s"
                cursor.execute(load_query, (self.restaurant_id,))
                record = cursor.fetchone()

                if record:
                    self.name = record['name']
                    self.phone_number = record['phoneNumber']
                    self.address = record['address']
                    self.second_address = record['secondAddress']
                    self.city = record['city']
                    self.state = record['state']
                    self.zip_code = record['zipCode']
                    self.website = record['website']
                    self.user_id = record['userId']
                else:
                    raise Exception("Error: this restaurant does not exist in the database")

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor()
                delete_reviews_query = "DELETE FROM Review WHERE restaurantId = %s"
                cursor.execute(delete_reviews_query, (self.restaurant_id,))
                connection.commit()

                delete_restaurant_query = "DELETE FROM Restaurant WHERE restaurantId = %s"
                cursor.execute(delete_restaurant_query, (self.restaurant_id,))
                connection.commit()

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def restaurant_exists(restaurant_id):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                exists_query = "SELECT * FROM Restaurant WHERE restaurantId = %s"
                cursor.execute(exists_query, (restaurant_id,))
                return cursor.rowcount != 0

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def restaurant_exists_by_name_address(name, address, second_address, city, state, zip_code, restaurant_id=None):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='Hotel_Review',
                                                 user='root',
                                                 password='pass')

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)

                if restaurant_id is None:
                    if second_address is not None:
                        exists_query = """SELECT * FROM Restaurant 
                                          WHERE name = %s AND address = %s AND secondAddress = %s AND city = %s AND state = %s AND zipCode = %s"""
                        cursor.execute(exists_query, (name, address, second_address, city, state, zip_code))
                    else:
                        exists_query = """SELECT * FROM Restaurant 
                                          WHERE name = %s AND address = %s AND city = %s AND state = %s AND zipCode = %s"""
                        cursor.execute(exists_query, (name, address, city, state, zip_code))
                else:
                    if second_address is not None:
                        exists_query = """SELECT * FROM Restaurant 
                                          WHERE name = %s AND address = %s AND secondAddress = %s AND city = %s AND state = %s AND zipCode = %s AND restaurantId != %s"""
                        cursor.execute(exists_query, (name, address, second_address, city, state, zip_code, restaurant_id))
                    else:
                        exists_query = """SELECT * FROM Restaurant 
                                          WHERE name = %s AND address = %s AND city = %s AND state = %s AND zipCode = %s AND restaurantId != %s"""
                        cursor.execute(exists_query, (name, address, city, state, zip_code, restaurant_id))

                return cursor.rowcount != 0

        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()