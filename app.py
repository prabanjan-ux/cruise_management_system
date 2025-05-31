from flask import Flask, render_template, request, redirect, flash, url_for,session
from flask_mysql_connector import MySQL
from MySQLdb.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuring MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Chitra@143'
app.config['MYSQL_DATABASE'] = 'cruise_management'
app.config['MYSQL_HOST'] = 'localhost'


# Initialize MySQL
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/passenger_login',methods=['GET','POST'])
def passenger_login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        cur = mysql.connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM register WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('passenger'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('passenger_login'))

    return render_template('passenger_login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']

        cur = mysql.connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM admin_login WHERE id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()

        if admin and admin['password'] == admin_password:  # if you stored plain text
            # If using hashed passwords, use check_password_hash(admin['password'], admin_password)
            session['admin_id'] = admin['id']
            return redirect(url_for('cruise'))  # make sure this route exists
        else:
            flash('Invalid Admin ID or Password')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')



@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. Please login.')
        return redirect(url_for('passenger_login'))

    return render_template('register.html')


@app.route('/passenger', methods=['GET', 'POST'])
def passenger():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        passport_number = request.form['passport_number']
        country = request.form['country']
        phone_number = request.form.get('phone_number', '')  # optional
        gender = request.form['gender']

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Passenger (name, passport_number, country, phone_number, gender)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, passport_number, country, phone_number, gender))
            mysql.connection.commit()
            cur.close()
            flash('Passenger added successfully!')
        except Exception as e:
            flash(f'Error adding passenger: {str(e)}')

        return redirect(url_for('passenger'))

    return render_template('passenger.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    cur = mysql.connection.cursor(dictionary=True)

    # For displaying cruises
    cur.execute("""
        SELECT
            c.cruise_id,
            c.cruisename,
            dp.port_name AS departure_port,
            ap.port_name AS arrival_port,
            c.departure_date,
            c.arrival_date,
            c.duration_of_days
        FROM cruise c
        LEFT JOIN port dp ON c.departure_port_id = dp.port_id
        LEFT JOIN port ap ON c.arrival_port_id = ap.port_id
    """)
    cruises = cur.fetchall()

    # Handle booking submission
    if request.method == 'POST':
        cruise_id = request.form['cruise_id']
        passenger_id = request.form['passenger_id']

        try:
            cur.execute("""
                INSERT INTO booking (passenger_id, cruise_id)
                VALUES (%s, %s)
            """, (passenger_id, cruise_id))
            mysql.connection.commit()

            flash('Booking successful!')
        except Exception as e:
            flash(f'Error booking cruise: {str(e)}')

        return redirect(url_for('booking'))

    cur.close()
    return render_template('booking.html', cruises=cruises)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        cruise_id = request.form.get('cruise_id')

        cur = mysql.connection.cursor(dictionary=True)
        cur.execute("""
    SELECT
        c.cruise_id,
        c.cruisename,
        dp.port_name AS departure_port,
        ap.port_name AS arrival_port,
        c.departure_date,
        c.arrival_date,
        c.duration_of_days,
        c.cost
    FROM cruise c
    LEFT JOIN port dp ON c.departure_port_id = dp.port_id
    LEFT JOIN port ap ON c.arrival_port_id = ap.port_id
    WHERE c.cruise_id = %s
""", (cruise_id,))

        cruise_details = cur.fetchone()
        cur.close()

        return render_template('payment.html', cruise=cruise_details)

    # If somehow someone lands here via GET
    flash('Invalid access to payment page.')
    return redirect(url_for('booking'))



@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    cruise_id = request.form.get('cruise_id')
    passengers = request.form.get('passengers')
    total_amount = request.form.get('total_amount')
    payment_method = request.form.get('payment_method')
    passenger_id = session.get('passenger_id')

    print("---- FORM DEBUG ----")
    print("cruise_id:", cruise_id)
    print("passengers:", passengers)
    print("total_amount:", total_amount)
    print("payment_method:", payment_method)
    print("passenger_id (from session):", passenger_id)
    print("---------------------")

    if not all([cruise_id, passengers, total_amount, payment_method, passenger_id]):
        flash("Incomplete booking data.")
        return redirect(url_for('booking'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO booking (passenger_id, cruise_id, num_passengers, total_amount, payment_method)
            VALUES (%s, %s, %s, %s, %s)
        """, (passenger_id, cruise_id, passengers, total_amount, payment_method))
        mysql.connection.commit()
        cur.close()

        flash('Booking confirmed successfully!')
    except Exception as e:
        print("DB INSERT ERROR:", e)
        flash(f"Database error: {str(e)}")

    return redirect(url_for('booking'))




@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        passenger_id = request.form['passenger_id']
        message = request.form['message']
        rating = request.form['rating']

        # Basic validation
        if not passenger_id or not message or not rating:
            flash('All fields are required.')
            return redirect(url_for('feedback'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO feedback (passenger_id, feedback, rating)
                VALUES (%s, %s, %s)
            """, (passenger_id, message, rating))
            mysql.connection.commit()
            cur.close()
            flash('Thank you for your feedback!')
        except Exception as e:
            flash(f'Error submitting feedback: {str(e)}')

        return redirect(url_for('feedback'))

    return render_template('feedback.html')



@app.route('/cruise', methods=['GET', 'POST'])
def cruise():
    cur = mysql.connection.cursor()
    cur.execute("SELECT port_id, port_name FROM port")
    ports = cur.fetchall()
    cur.close()

    port_names = [port[1] for port in ports]

    if request.method == 'POST':
        cruise_name = request.form['cruise_name']
        departure_port_name = request.form['departure_port']
        arrival_port_name = request.form['arrival_port']
        departure_date = request.form['departure_date']
        arrival_date = request.form['arrival_date']
        duration_days = request.form['duration_days']
        cost = request.form['cost']


        try:
            cur = mysql.connection.cursor(dictionary=True)

            # Fetch port IDs
            cur.execute("SELECT port_id FROM port WHERE port_name = %s", (departure_port_name,))
            departure_port = cur.fetchone()

            cur.execute("SELECT port_id FROM port WHERE port_name = %s", (arrival_port_name,))
            arrival_port = cur.fetchone()

            if not departure_port or not arrival_port:
                flash('Invalid port selection.')
                return redirect(url_for('cruise'))

            departure_port_id = departure_port['port_id']
            arrival_port_id = arrival_port['port_id']

            # Insert into Cruise
            cur.execute("""
                INSERT INTO cruise (cruisename, departure_port_id, arrival_port_id, departure_date, arrival_date, duration_of_days, cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (cruise_name, departure_port_id, arrival_port_id, departure_date, arrival_date, duration_days, cost))

            mysql.connection.commit()
            cur.close()

            flash('Cruise added successfully!')
            return redirect(url_for('cruise'))

        except Exception as e:
            flash(f'Error adding cruise: {str(e)}')
            return redirect(url_for('cruise'))

    return render_template('cruise.html', port_names=port_names)




@app.route('/port', methods=['GET', 'POST'])
def port():
    print("Form request method:", request.method)  # <--- Check if form is submitting

    if request.method == 'POST':
        port_name = request.form['port_name']
        country = request.form['country']
        print(f"Submitted: {port_name}, {country}")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO port (port_name, country) VALUES (%s, %s)", (port_name, country))
        mysql.connection.commit()
        cur.close()

        flash('Port added successfully!')
        return redirect(url_for('port'))

    return render_template('port.html')



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)