CREATE DATABASE bingoo;

USE bingoo;

CREATE TABLE keyword (
  id INT PRIMARY KEY AUTO_INCREMENT,
  keyword VARCHAR(255) NOT NULL
);

CREATE TABLE indexed_links (
  id INT PRIMARY KEY AUTO_INCREMENT,
  keyword_id INT,
  link VARCHAR(1000) NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keyword(id)
);
