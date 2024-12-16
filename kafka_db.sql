DROP DATABASE IF EXISTS Kafka_db;
CREATE DATABASE Kafka_db;
USE Kafka_db;
CREATE TABLE Coordinates(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    IP INT, 
	latitude FLOAT,
    longitude FLOAT,
    messageDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);