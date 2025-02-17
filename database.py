import mysql.connector

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="password",
        database="manuDB"
    )

# initializing the database
def initialize_database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_cvp(
            prod_id INT PRIMARY KEY AUTO_INCREMENT,
            comp_id INT,
            fixed_cost DECIMAL(15,2),
            variable_cost_per_unit DECIMAL(10,2),
            selling_price_per_unit DECIMAL(10,2),
            target_income DECIMAL(15,2)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            comp_id INT,
            fname VARCHAR(15),
            lname VARCHAR(15),
            email VARCHAR(20),
            password VARCHAR(255),
            username VARCHAR(255) UNIQUE
        );
        """)

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

# Add a user to the database
def add_user_to_database(username, security_level, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO user (username, security_level, password)
        VALUES (%s, %s, %s);
        """, (username, security_level, password))

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")

# Get a user by username
def get_username_from_database(username):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
        SELECT user_id, username, password, security_level 
        FROM user 
        WHERE username = %s;
        """, (username,))

        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result  # Will return None if user not found

    except mysql.connector.Error as err:
        print(f"Error fetching user: {err}")
        return None
