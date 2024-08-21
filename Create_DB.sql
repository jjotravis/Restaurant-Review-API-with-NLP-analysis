CREATE DATABASE IF NOT EXISTS Hotel_Review;

USE Hotel_Review;

CREATE TABLE IF NOT EXISTS Restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    cuisine VARCHAR(50)
);

CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES Restaurants(restaurant_id),
    user_id INT,
    review_text TEXT,
    sentiment VARCHAR(10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Users (
    
)