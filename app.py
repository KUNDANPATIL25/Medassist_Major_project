from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Doctor
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use env variables in production

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB with app
db.init_app(app)

# Home (Splash / Landing)
@app.route('/')
def home():
    return render_template('index.html')

# Doctor Registration
@app.route('/register-doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        license_number = request.form['license_number']
        location = request.form['location']
        affiliation = request.form['affiliation']
        specialization = request.form['specialization']

        if Doctor.query.filter_by(email=email).first():
           msg = "Email already registered, Please Login ."
           return render_template('login.html', message=msg)

        doctor = Doctor(
            full_name=full_name,
            email=email,
            phone=phone,
            password=password,
            specialization=specialization,
            license_number=license_number,
            location=location,
            affiliation=affiliation,
            created_at=datetime.utcnow()
        )

        db.session.add(doctor)
        db.session.commit()

        session['user_id'] = doctor.id
        session['user_name'] = doctor.full_name
        session['user_type'] = 'doctor'
        flash("Doctor registered successfully!", "success")
        return redirect(url_for('dashboard_doctor'))

    return render_template('doctor_register.html')

# Doctor Dashboard
@app.route('/dashboard-doctor')
def dashboard_doctor():
    if 'user_id' not in session or session.get('user_type') != 'doctor':
        flash("Access denied. Please login as a doctor.", "error")
        return redirect(url_for('login'))

    doctor = Doctor.query.get(session['user_id'])
    if not doctor:
        flash("Doctor not found.", "error")
        return redirect(url_for('login'))

    return render_template('dashboard_doctor.html', doctor=doctor)

# User Registration
@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        landmark = request.form['landmark']
        location = request.form['location']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        condition = request.form['condition']
        medications = request.form['medications']
        allergies = request.form['allergies']

        if User.query.filter_by(email=email).first():
            msg = "Email already registered, Please Login ."
            return render_template('login.html',message=msg)

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            landmark=landmark,
            location=location,
            password=password,
            age=age,
            gender=gender,
            condition=condition,
            medications=medications,
            allergies=allergies,
            created_at=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['user_name'] = user.full_name
        session['user_type'] = 'user'

        flash("User registered successfully!", "success")
        return redirect(url_for('dashboard_user'))

    return render_template('user_register.html')


@app.route('/dashboard-user')
def dashboard_user():
    if 'user_id' not in session or session.get('user_type') != 'user':
        flash("Unauthorized access. Please login.", "error")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('login'))

    return render_template('dashboard_user.html', user=user)



# Login Route (for both doctor and user)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        doctor = Doctor.query.filter_by(email=email, password=password).first()
        user = User.query.filter_by(email=email, password=password).first()

        if doctor:
            session['user_id'] = doctor.id
            session['user_name'] = doctor.full_name
            session['user_type'] = 'doctor'
            flash('Doctor logged in successfully!', 'success')
            return redirect(url_for('dashboard_doctor'))

        elif user:
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['user_type'] = 'user'
            flash("User logged in successfully!", "success")
            return redirect(url_for('dashboard_user'))

        else:
            msq= "Invalid email or password. Please try again."
            return render_template('login.html', message=msq)
            

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
