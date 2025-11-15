from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import init_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
mongo = init_db(app)


# --------------------
# Routes
# --------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/doctors')
def doctors_page():
    doctors = list(mongo.db.doctors.find())
    # Convert ObjectId to string for session-safe rendering
    for doc in doctors:
        doc['_id'] = str(doc['_id'])
    return render_template('doctors.html', doctors=doctors)



@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        flash("Please login to access appointments.", "warning")
        return redirect(url_for('login'))
    return render_template('appointments.html')


@app.route('/records')
def records():
    if 'user_id' not in session:
        flash("Please login to access health records.", "warning")
        return redirect(url_for('login'))
    return render_template('records.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        mongo.db.messages.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
            "created_at": datetime.utcnow()
        })
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password.", "danger")
            return render_template('login.html')

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
            flash("Email already exists.", "danger")
            return render_template('register.html')

        password_hashed = generate_password_hash(password)

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": password_hashed,
            "phone": phone,
            "created_at": datetime.utcnow()
        })

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


# --------------------
# Run app
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
