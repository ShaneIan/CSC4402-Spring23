CREATE DATABASE IF NOT EXISTS contact_management;
USE contact_management;

CREATE TABLE IF NOT EXISTS contacts (
	id 			INT(11) NOT NULL AUTO_INCREMENT,
	name 		VARCHAR(255) NOT NULL,
	email 		VARCHAR(255) NOT NULL,
	phone 		VARCHAR(255) NOT NULL,
	address 	VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
);

INSERT INTO contacts (name, email, phone, address) VALUES ('John Smith', 'john@example.com', '555-1234', '123 Main St');
INSERT INTO contacts (name, email, phone, address) VALUES ('Jane Doe', 'jane@example.com', '555-5678', '456 Maple St');
