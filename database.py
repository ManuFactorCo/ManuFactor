import mysql.connector
from encryption import cipher

def initialize_database():
    # initialize the database and adds default users if they don't already exist. 
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor()


    # create product  table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_cvp (
        prod_id INT PRIMARY KEY AUTO_INCREMENT,
        comp_id INT,
        fixed_cost DECIMAL(15,2),
        variable_cost_per_unit DECIMAL(10,2),
        selling_price_per_unit DECIMAL(15,2),
        target_income DECIMAL(15,2)
    );
    """)

    # Create User table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        comp_id INT,
        fname VARCHAR(255),
        lname VARCHAR(255),
        email VARCHAR(255),
        security_level INT,
        password VARCHAR(255),
        Username VARCHAR(255) UNIQUE
    );
    """)

    # adding the default users if they don't already exist
    cursor.execute("SELECT * FROM user WHERE Username = %s", (cipher.encrypt(b"admin").decode(),))
    if cursor.fetchone() is None:
        add_user_to_database(cursor, "admin", "admin", 3)

    cursor.execute("SELECT * FROM user WHERE Username = %s", (cipher.encrypt(b"user").decode(),))
    if cursor.fetchone() is None:
        add_user_to_database(cursor, "user", "user", 2)

    cursor.execute("SELECT * FROM user WHERE Username = %s", (cipher.encrypt(b"viewer").decode(),))
    if cursor.fetchone() is None:
        add_user_to_database(cursor, "viewer", "viewer", 1)

    connection.commit()
    cursor.close()
    connection.close()

def add_user_to_database(cursor, username, password, security_level):
    """ Adds a new user to the database with encrypted password. """
    encrypted_password = cipher.encrypt(password.encode()).decode()
    cursor.execute("""
    INSERT INTO user (username, lname, email, security_level, password)
    VALUES (%s, %s, %s, %s, %s)
    """, (username, username, f"{username}@example.com", security_level, encrypted_password))


'''def get_username_from_database(encrypted_username):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (encrypted_username,))
    user = cursor.fetchone()

    #if user:
       # print("Stored Encrypted Username in DB:", user['username'])  # Debugging line

    cursor.close()
    connection.close()
    return user'''
def get_username_from_database(encrypted_username):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor(dictionary=True)

    query = "SELECT user_id AS ID, username AS Username, password AS Password, security_level AS Security FROM user WHERE username = %s"
    cursor.execute(query, (encrypted_username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()
    return user
