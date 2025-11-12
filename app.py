from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import create_connection, init_db
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
init_db()

@app.route('/')
def index():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get featured doctors
    cursor.execute("SELECT * FROM doctors LIMIT 3")
    featured_doctors = cursor.fetchall()
    
    # Get services
    cursor.execute("SELECT * FROM services LIMIT 6")
    services = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('index.html', 
                         featured_doctors=featured_doctors, 
                         services=services)

@app.route('/services')
def services():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('services.html', services=services)

@app.route('/doctors')
def doctors():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        service_id = request.form['service_id']
        pet_id = request.form['pet_id']
        date = request.form['date']
        time = request.form['time']
        
        cursor.execute('''
            INSERT INTO appointments (user_id, doctor_id, service_id, pet_id, date, time)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (session['user_id'], doctor_id, service_id, pet_id, date, time))
        
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('appointments'))
    
    # Get user's pets
    cursor.execute("SELECT * FROM pets WHERE user_id = %s", (session['user_id'],))
    pets = cursor.fetchall()
    
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    
    # Get user appointments
    cursor.execute('''
        SELECT a.*, d.name as doctor_name, s.name as service_name, p.name as pet_name
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN services s ON a.service_id = s.id
        JOIN pets p ON a.pet_id = p.id
        WHERE a.user_id = %s
        ORDER BY a.date DESC, a.time DESC
    ''', (session['user_id'],))
    user_appointments = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('appointments.html', 
                         pets=pets, 
                         doctors=doctors, 
                         services=services,
                         appointments=user_appointments)

@app.route('/records')
def records():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM pets WHERE user_id = %s", (session['user_id'],))
    pets = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('records.html', pets=pets)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        
        connection = create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, phone)
                VALUES (%s, %s, %s, %s)
            ''', (name, email, password, phone))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            cursor.close()
            connection.close()
            return render_template('register.html', error='Email already exists')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add_pet', methods=['POST'])
def add_pet():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form['name']
    species = request.form['species']
    breed = request.form['breed']
    age = request.form['age']
    weight = request.form['weight']
    medical_history = request.form['medical_history']
    
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO pets (user_id, name, species, breed, age, weight, medical_history)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (session['user_id'], name, species, breed, age, weight, medical_history))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('records'))

if __name__ == '__main__':
    app.run(debug=True)