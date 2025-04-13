"""C. MILLS: FLASK IS ACCURATE, DB IS ACCURATE, CONNECTION NEEDS TO BE RESOLVED."""
import mysql.connector
from encryption import cipher

def initialize_database():
    # initialize the database and adds default users if they don't already exist. 
    '''connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor()''' #LD REMOVED

    #LD ADDING PART BELOW
    # Step 1: connect without specifying the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = connection.cursor()

    # Step 2: create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS manuDB")
    connection.commit()
    cursor.close()
    connection.close()

    # Step 3: connect to the newly created database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor()

    #LD ADDING PART ABOVE

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

    # create product table (if not exists)
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

    # Add default users if they don't exist
    admin_user = "admin"
    encrypted_admin_username = cipher.encrypt(admin_user.encode()).decode()
    cursor.execute("SELECT * FROM user WHERE Username = %s", (encrypted_admin_username,))
    if cursor.fetchone() is None:
        encrypted_password = cipher.encrypt(admin_user.encode()).decode()
        cursor.execute("""
        INSERT INTO user (username, lname, email, security_level, password)
        VALUES (%s, %s, %s, %s, %s)
        """, (encrypted_admin_username, admin_user, f"{admin_user}@example.com", 3, encrypted_password))

    user_user = "user"
    encrypted_user_username = cipher.encrypt(user_user.encode()).decode()
    cursor.execute("SELECT * FROM user WHERE Username = %s", (encrypted_user_username,))
    if cursor.fetchone() is None:
        encrypted_password = cipher.encrypt(user_user.encode()).decode()
        cursor.execute("""
        INSERT INTO user (username, lname, email, security_level, password)
        VALUES (%s, %s, %s, %s, %s)
        """, (encrypted_user_username, user_user, f"{user_user}@example.com", 2, encrypted_password))

    viewer_user = "viewer"
    encrypted_viewer_username = cipher.encrypt(viewer_user.encode()).decode()
    cursor.execute("SELECT * FROM user WHERE Username = %s", (encrypted_viewer_username,))
    if cursor.fetchone() is None:
        encrypted_password = cipher.encrypt(viewer_user.encode()).decode()
        cursor.execute("""
        INSERT INTO user (username, lname, email, security_level, password)
        VALUES (%s, %s, %s, %s, %s)
        """, (encrypted_viewer_username, viewer_user, f"{viewer_user}@example.com", 1, encrypted_password))

    connection.commit()
    cursor.close()
    connection.close()



def add_user_to_database(cursor, username, password, security_level):
    """ Adds a new user to the database with encrypted password and username. """
    encrypted_username = cipher.encrypt(username.encode()).decode()  # Encrypt username
    encrypted_password = cipher.encrypt(password.encode()).decode()  # Encrypt password
    
    cursor.execute("""
    INSERT INTO user (username, lname, email, security_level, password)
    VALUES (%s, %s, %s, %s, %s)
    """, (encrypted_username, username, f"{username}@example.com", security_level, encrypted_password))


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

'''def get_username_from_database(encrypted_username):
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
    return user''' #LD REMOVED 

    #LD ADDED PART BELOW
def get_username_from_database(encrypted_username):
    # Create DB if it doesn't exist (safe fallback)
    temp_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute("CREATE DATABASE IF NOT EXISTS manuDB")
    temp_conn.commit()
    temp_cursor.close()
    temp_conn.close()

    # Now connect to the real DB
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

    #LD ADDED PART ABOVE

