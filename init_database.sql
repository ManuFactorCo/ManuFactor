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

CREATE TABLE product_bp (
    prod_id INT PRIMARY KEY AUTO_INCREMENT,
    comp_id INT NOT NULL CHECK (comp_id > 0),
    curr_Sales INT NOT NULL CHECK (curr_Sales > 0),
    next_Sales INT NOT NULL CHECK (next_Sales > 0),
    twicenext_Sales INT NOT NULL CHECK (twicenext_Sales > 0),
    EI_Rate DECIMAL(10,2) NOT NULL CHECK (EI_Rate > 0),
    DM_per_Unit INT NOT NULL CHECK (DM_per_Unit > 0),
    EI_DM_Rate DECIMAL(10,2) NOT NULL CHECK (EI_DM_Rate > 0),
    DM_Price DECIMAL(10,2) NOT NULL CHECK (DM_Price > 0)
);
