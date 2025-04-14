"""C. MILLS: FLASK IS ACCURATE, DB IS ACCURATE, CONNECTION NEEDS TO BE RESOLVED."""

"""
USING FLASK, HTML, SQL DATABASE, CIPHER TO IMPLEMENT ROLE BASED ACCESS CONTROL AND ENCRYPTION.
INSTALL FLASK, CIPHER.
"""

#IMPORT
import mysql.connector #LD IS ADDING
from flask import Flask, render_template, redirect, url_for, request, session
from database import initialize_database, add_user_to_database, get_username_from_database #IMPLEMENT DATABASE FUNCTIONS
from encryption import cipher

#FLASK
app = Flask(__name__)
app.secret_key = 'secret_key'

#LD adding part below
initialize_database()

#this should effectively make username a global variable
#any template should now be able to refer to the username of whoever is logged in via {{username}}
@app.context_processor
def inject_user():
    return dict(username=session.get('username'))


#LD addding part above

"""C. MILLS: INITALIZE DB ONCE. 
#INITALIZE DATABASE
initialize_database()
"""

"""
#ADMIN TEST USER SECURITY LEVEL III 
add_user_to_database("admin", 3, cipher.encrypt("admin".encode()).decode())

#USER TEST USER SECURITY LEVEL II
add_user_to_database("user", 2, cipher.encrypt("user".encode()).decode())

#VIEWER TEST USER SECURITY LEVEL I
add_user_to_database("viewer", 1, cipher.encrypt("viewer".encode()).decode())
"""

#LOGIN FUNCTION
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encrypted_username = cipher.encrypt(username.encode()).decode()  # Encrypt username
        
        # Fetch user from DB
        user = get_username_from_database(encrypted_username)

        # Check if password matches the decrypted stored password
        if user:
            decrypted_password = cipher.decrypt(user['Password'])  # Decrypt stored password
            if decrypted_password == password:
                session['ID'] = user['ID']
                session['username'] = cipher.decrypt(user['Username'])  # Decrypt the username if needed
                session['security'] = user['Security']
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="INVALID PASSWORD.")  # Password mismatch
        else:
            return render_template('login.html', error="USER NOT FOUND.")  # User not found

    return render_template('login.html')


#LOGOUT FUNCTION
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#HOME PAGE FUNCTION
@app.route('/')
def home():
    if 'ID' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'], security=session['security'])

#RESULTS PAGE FUNCTION
@app.route('/results')
def results():
    return render_template('results.html', message=request.args.get('message', ''))

#VIEWER, USER, ADMIN FUNCTION VIEW DATA
@app.route('/list_data')
def list_data():
    if 'ID' not in session:
        return redirect(url_for('login'))
    if session['security'] >= 1: 
        #IMPLEMENT DATABASE LOGIC
        data = []  
        return render_template('list_data.html', data=data)
    return redirect(url_for('login'))

#USER, ADMIN FUNCTION ADD DATA 
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if 'ID' not in session:
        return redirect(url_for('login'))
    if session['security'] >= 2: 
        if request.method == 'POST':
            #IMPLEMENT DATABASE LOGIC
            return redirect(url_for('results', message="RECORD ADDED."))
        return render_template('add_data.html')
    return redirect(url_for('login'))

#ADMIN FUNCTION LIST USER
@app.route('/list_users')
def list_users():
    if 'ID' not in session or session['security'] < 3:
        return redirect(url_for('login'))
    
    # Connect to the database and get a cursor
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manuDB"
    )
    cursor = connection.cursor(dictionary=True)

    # Fetch all users from the database
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()

    # Decrypt the usernames and update the user dictionary
    for user in users:
        user['Username'] = cipher.decrypt(user['Username'])  # Decrypt the username

    # Close the connection
    cursor.close()
    connection.close()

    return render_template('list_users.html', users=users)


#ADMIN FUNCTION ADD USER
'''@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'ID' not in session or session['security'] >= 3:  #LD changed security_level to security
        if request.method == 'POST':
            #IMPLEMENT DATABASE LOGIC
            username = request.form['username'] #LD changing name to username
            security_level = int(request.form['role'])# LD changing security level to role
            password = cipher.encrypt(request.form['login_password'].encode()).decode()
            add_user_to_database(username, security_level, password)#LD changing name to username
            return redirect(url_for('results', message="USER ADDED."))
        return render_template('add_users.html') #LD changed add_user.html to add_user
    return redirect(url_for('login'))''' #LD REMOVED

    #LD ADDING PART BELOW
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'ID' not in session or session['security'] >= 3:
        if request.method == 'POST':
            # Get the form values
            username = request.form['username']
            security_level = int(request.form['role'])  # Get the role as the security level
            password = request.form['login_password']

            # Connect to the database and get a cursor
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="manuDB"
            )
            cursor = connection.cursor()

            # Add the user to the database
            add_user_to_database(cursor, username, password, security_level)

            # Commit the changes and close the connection
            connection.commit()
            cursor.close()
            connection.close()

            # Redirect after adding the user
            return redirect(url_for('home', message="USER ADDED."))
        return render_template('add_users.html')  # Display the form if it's a GET request
    return redirect(url_for('login'))  # Redirect if not an admin


    #LD ADDING PART ABOVE



#ADDING ROUTES ALONGSIDE HTML

#MAIN FUNCTION
if __name__ == '__main__':
    app.run(debug=True)
