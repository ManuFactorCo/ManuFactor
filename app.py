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
from get_comp_id import get_company_id_by_username
from product_cvp import update_product_cvp, calc_cvp_summary
from product_bp import update_product_bp, calc_bp_summary

#FLASK
app = Flask(__name__)
app.secret_key = 'secret_key'

#LD adding part below
initialize_database()

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
            #EVERYTHING BETWEEN THIS AND 
            username = session.get('username')
            if not username:
                return redirect(url_for('login'))
                #redirects to login if no username
            comp_id = get_company_id_by_username(username)
            if not comp_id:
                return "Company ID not found", 404
                #error if not comp_id
            if 'fixed_costs' in request.form:
                #this means they are trying to update the cvp info
                 try:
                    fixed_cost = float(request.form['fixed_costs'])
                    variable_cost = float(request.form['variable-cost-per-unit'])
                    selling_price = float(request.form['selling-price-per-unit'])
                    target_income = float(request.form['projected-units'])

                    update_product_cvp(
                        company_id=comp_id,
                        fixed_cost=fixed_cost,
                        variable_cost_per_unit=variable_cost,
                        selling_price_per_unit=selling_price,
                        target_income=target_income
                    )

                    return redirect(url_for('results', message="CVP data updated."))

                    except ValueError:
                     return "Invalid input values", 400    
            elif 'curr_Sales' in request.form:
                #this means they are trying to update the bp info
                try:
                    curr_sales = int(request.form['curr_Sales'])
                    next_sales = int(request.form['next_Sales'])
                    twicenext_sales = int(request.form['twicenext_Sales'])
                    ei_rate = float(request.form['EI_Rate']) / 100  # Convert % to decimal
                    dm_per_unit = float(request.form['DM_per_Unit'])
                    ei_dm_rate = float(request.form['EI_DM_Rate']) / 100  # Convert % to decimal
                    dm_price = float(request.form['DM_Price'])

                    update_product_bp(
                        company_id=comp_id,
                        curr_Sales=curr_sales,
                        next_Sales=next_sales,
                        twicenext_Sales=twicenext_sales,
                        EI_Rate=ei_rate,
                        DM_per_Unit=dm_per_unit,
                        EI_DM_Rate=ei_dm_rate,
                        DM_Price=dm_price
                    )

                    return redirect(url_for('results', message="BP data updated."))

                except ValueError:
                    return "Invalid BP input values", 404  
                #THIS WAS JUST ADDED
                #requires testing but should handle updating the table
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

#SB - ADDING ROUTE SKELETON FROM TXT
@app.route('/cvp_summary')
def cvp_summary():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    comp_id = get_company_id_by_username(username)
    if not comp_id:
        return "Company ID not found", 404

    summary = calc_cvp_summary(comp_id)
    if not summary:
        return "No CVP data available", 404
    if "error" in summary:
        return f"Error: {summary['error']}", 400

    #passes data to template, can reference as attributes of summary
    #EX: to reference breakeven point in units use summary.breakeven_units
    return render_template('cvp_summary.html', summary=summary)


@app.route('/bp_summary')
def bp_summary():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    comp_id = get_company_id_by_username(username)
    if not comp_id:
        return "Company ID not found", 404

    summary = calc_bp_summary(comp_id)
    if not summary:
        return "No BP data available.", 404
    if "error" in summary:
        return f"Error: {summary['error']}", 400
    #passes data to template can reference as attributes of summary
    #EX to reference required production, use summary.production_required
    return render_template('bp_summary.html', summary=summary)
#SB - ADDING ROUTE SKELETON FROM TXT

#NOTES FROM ANTONIO REGARDING RESULT OUTPUT
#I am not sure where you are intending on having results displayed but essentially in 
#whatever route we will call summary=calc_cvp_summary or summary=calc_bp_summary
#then pass summary as an argument into render template, this should then make the
#results of my back end function usable in the templates
#EX: in a route that is for cvp results, app.py passes summary as an argument
#in the template you could display the result of breakeven point in units as 
# <p><strong>Breakeven Point (Units):</strong> {{ summary.breakeven_units }}</p>
#once i know what exact routes are being used for cvp and bp result display
#i will write the logic to pass summary into the template
#ADDING ROUTES ALONGSIDE HTML

#MAIN FUNCTION
if __name__ == '__main__':
    app.run(debug=True)
