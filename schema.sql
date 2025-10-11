CREATE DATABASE IF NOT EXISTS village_waste;
USE village_waste;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  role ENUM('user','admin') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  complaint_date DATE NOT NULL,
  waste_type VARCHAR(50),
  description TEXT,
  status ENUM('Pending','Collected') DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

USE village_waste;

INSERT INTO users (name, email, password, address, role)
VALUES (
  'Admin',
  'admin@village.local',
  'scrypt:32768:8:1$2dj8OkvnX7zXrbrq$dd19d8c3bea404b1357763831f05c12a9d804b94de422df98c62acb8b9400805f66357af1481077f980e7316b1d2bc0666fddd6a54701548eee357c0fcc36816', 
  'Head Office',
  'admin'
);



select * from users

