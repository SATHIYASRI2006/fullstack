CREATE DATABASE marksheet_db;

USE marksheet_db;

CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_mark INT,
    image_path VARCHAR(255)
);
