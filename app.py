from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register-doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['fullName']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        license = request.form['license']
        specialization = request.form['specialization']
        affiliation = request.form['affiliation']
        certificate = request.files['certificate']

        filename = secure_filename(certificate.filename)
        certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Doctor registered successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('doctor_register.html')

@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Capture user form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        condition = request.form['condition']
        medications = request.form['medications']
        allergies = request.form['allergies']
        user_type = request.form['userType']

        flash('User registered successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('user_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email and password:
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
