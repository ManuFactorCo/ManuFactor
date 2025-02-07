"""
Name: SAMANTHA BUI
USING FLASK, HTML, SQL DATABASE, CIPHER TO IMPLEMENT ROLE BASED ACCESS CONTROL AND ENCRYPTION.
"""

"""
INSTALL FLASK, CIPHER
RUN ON LINPROG
"""

#IMPORT
from flask import Flask, render_template, redirect, url_for, request, session
from database import initialize_database, add_user_to_database, get_username_from_database #IMPLEMENT DATABASE FUNCTIONS
from encryption import cipher

#FLASK
app = Flask(__name__)
app.secret_key = 'secret_key'

#INITALIZE DATABASE
initialize_database()

#ADMIN TEST USER SECURITY LEVEL III 
add_user_to_database("admin", 3, cipher.encrypt("admin".encode()).decode())

#USER TEST USER SECURITY LEVEL II
add_user_to_database("user", 2, cipher.encrypt("user".encode()).decode())

#VIEWER TEST USER SECURITY LEVEL I
add_user_to_database("viewer", 1, cipher.encrypt("viewer".encode()).decode())

#LOGIN FUNCTION
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encrypted_username = cipher.encrypt(username.encode()).decode()
        user = get_username_from_database(encrypted_username)
        if user and cipher.decrypt(user['Password']) == password:
            session['ID'] = user['ID']
            session['username'] = cipher.decrypt(user['Username'])
            session['security'] = user['Security']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="INVALID.")
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
    if 'ID' not in session or session['security'] >= 3:  
        #IMPLEMENT DATABASE LOGIC
        users = []
        return render_template('list_users.html', users=users)
    return redirect(url_for('login'))

#ADMIN FUNCTION ADD USER
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'ID' not in session or session['security_level'] >= 3:  
        if request.method == 'POST':
            #IMPLEMENT DATABASE LOGIC
            name = request.form['name']
            security_level = int(request.form['security_level'])
            password = cipher.encrypt(request.form['login_password'].encode()).decode()
            add_user_to_database(name, security_level, password)
            return redirect(url_for('results', message="USER ADDED."))
        return render_template('add_user.html')
    return redirect(url_for('login'))

#MAIN FUNCTION
if __name__ == '__main__':
    app.run(debug=True)
