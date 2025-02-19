import mysql.connector
from encryption import cipher

def initialize_database():
    # initialize the database and adds default users 
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor()



    # adding the default users 
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
