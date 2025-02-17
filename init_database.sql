-- Create CVP Database
CREATE DATABASE IF NOT EXISTS manuDB;
USE manuDB;

-- Create Product CVP Table
CREATE TABLE product_cvp(
	prod_id INT PRIMARY KEY AUTO_INCREMENT,
    comp_id INT,
    fixed_cost DECIMAL(15,2),
    variable_cost_per_unit DECIMAL(10,2),
    selling_price_per_unit DECIMAL(10,2),
    target_income DECIMAL(15,2)
);

-- Create User Table
CREATE TABLE user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    comp_id INT,
    fname VARCHAR(15),
    lname VARCHAR(15),
    email VARCHAR(20)
)
