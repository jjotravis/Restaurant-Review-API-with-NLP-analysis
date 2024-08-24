CREATE DATABASE IF NOT EXISTS Hotel_Review;

USE Hotel_Review;

CREATE TABLE IF NOT EXISTS Users(
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL, 
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL, 
  password VARCHAR(255) NOT NULL,
  zip_code VARCHAR(10),
  birthday DATE,
  phone_number VARCHAR(20), 
  gender VARCHAR(10),
  user_type VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Restaurants (
  restaurantId INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  phoneNumber VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  secondAddress VARCHAR(255),
  city VARCHAR(50) NOT NULL,
  state CHAR(2) NOT NULL, 
  zipCode CHAR(5) NOT NULL,
  website VARCHAR(255),
  userId INT,
  FOREIGN KEY (userId) REFERENCES Users(user_id) 
);

CREATE TABLE IF NOT EXISTS Reviews(
    review_id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES Restaurants(restaurant_id),
    user_id INT,
    review_text TEXT,
    sentiment VARCHAR(10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);