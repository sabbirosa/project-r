CREATE DATABASE project_r;

USE project_r;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    blood_group VARCHAR(5),
    email VARCHAR(100) UNIQUE,
    gender ENUM('Male', 'Female', 'Other'),
    password VARCHAR(255),
    status ENUM('Active', 'Banned') DEFAULT 'Active' NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    location VARCHAR(100),
    user_type ENUM('Staff', 'Donor', 'Admin') DEFAULT 'Donor' NOT NULL
);

CREATE TABLE diseases (
    disease_id INT AUTO_INCREMENT,
    disease_name VARCHAR(100),
    PRIMARY KEY (disease_id)
);

CREATE TABLE user_diseases (
    user_id INT,
    disease_id INT,
    PRIMARY KEY (user_id, disease_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (disease_id) REFERENCES diseases(disease_id) ON DELETE CASCADE
);

CREATE TABLE staff (
    role ENUM('Admin', 'Staff'),
    user_id INT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE donors (
    user_id INT PRIMARY KEY,
    last_donation_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE donations (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    proof_document VARCHAR(255),
    donated_date DATE,
    hospital_name VARCHAR(100),
    location VARCHAR(100),
    status ENUM('Processed', 'Unprocessed', 'Rejected'),
    request_id INT,
    donor_id INT,
    FOREIGN KEY (donor_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE blood_requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(100),
    location VARCHAR(100),
    is_fulfilled TINYINT(1) DEFAULT 0,
    urgency_level ENUM('Low', 'Medium', 'High'),
    requested_blood_group VARCHAR(5),
    reason VARCHAR(255),
    name VARCHAR(100),
    contact_information VARCHAR(255),
    need_by_date DATE,
    request_date DATE,
    requester_id INT,
    user_id INT,
    FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


CREATE TABLE violation_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    violator_id INT,
    reporter_id INT,
    report_date DATE,
    is_resolved TINYINT(1) DEFAULT 0,
    violation_reason TEXT,
    FOREIGN KEY (violator_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reporter_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Change the role of first registered user to donors to admin
UPDATE users SET user_type = 'Admin' WHERE user_id = 1;
INSERT INTO staff (user_id, role) VALUES (1, 'Admin');

