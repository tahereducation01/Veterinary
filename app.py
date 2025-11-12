from flask import Flask, render_template, request, redirect, url_for, session
from db import init_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
mongo = init_db(app)

@app.route('/')
def index():
    # For now, just render the homepage
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('appointments.html')

@app.route('/records')
def records():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('records.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Replace with MongoDB user check
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({"email": email, "password": password})
        if user:
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            return render_template('register.html', error="Email already exists")

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "phone": phone,
            "created_at": datetime.utcnow()
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
