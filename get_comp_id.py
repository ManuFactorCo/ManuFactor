import mysql.connector
from encryption import cipher

def get_company_id_by_username(username):
    """
    Encrypts the username and returns the corresponding comp_id from the user table.
    """
    if not username:
        return None

    encrypted_username = cipher.encrypt(username.encode()).decode()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manuDB"
        )
        cursor = connection.cursor()
        query = "SELECT comp_id FROM user WHERE username = %s"
        cursor.execute(query, (encrypted_username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0] if result else None

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
