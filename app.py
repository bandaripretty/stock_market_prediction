from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta
import yfinance as yf

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '1712'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:T%21m3L1n3%40Secure%232024@localhost:5433/stock_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for Flask-Login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=120)]) 
    email = StringField('Email', validators=[DataRequired(), Length(max=120), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=120)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# API for market trends data
@app.route('/api/market-trends')
@login_required
def market_trends_data():
    # Replace these values with actual values fetched from the database or yfinance
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']

    opening_prices = [125.6, 130.8, 145.3, 150.9, 160.5]
    high_prices = [130.6, 135.8, 150.3, 155.9, 165.5]
    low_prices = [120.1, 125.2, 140.1, 145.8, 155.3]
    closing_prices = [128.9, 132.3, 148.5, 153.2, 162.1]

    return jsonify({
        'opening_prices': opening_prices,
        'high_prices': high_prices,
        'low_prices': low_prices,
        'closing_prices': closing_prices
    })

@app.route('/market-trends')
@login_required
def market_trends():
    return render_template('market_trends.html')

@app.route('/archive')
@login_required
def archive():
    return render_template('archive.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        currency = request.form['currency']

        # Update user details (add your logic for updating in the database here)
        user = User.query.get(current_user.id)
        user.username = username
        user.email = email
        user.preferred_currency = currency
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()

        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html')

from flask import request, flash, redirect, url_for

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Email update
    if email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('This email is already taken by another user.', 'danger')
        else:
            current_user.email = email

    # Password update
    if current_password and new_password and confirm_password:
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            hashed_password = generate_password_hash(new_password)
            current_user.password = hashed_password
            flash('Your password has been updated successfully.', 'success')

    db.session.commit()

    return redirect(url_for('settings'))



@app.route('/help')
def help():
    return render_template('help.html')  # Render help page

@app.route('/support')
def support():
    return render_template('support.html')  # Render help page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Create a new user and store in the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/api/stock-data')
def all_stocks_data():
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    stock_data = {}

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='5d')
        stock_data[symbol] = {
            'latest_price': round(hist['Close'].iloc[-1], 2),
            'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            'closing_prices': hist['Close'].tolist(),
            'volumes': hist['Volume'].tolist()
        }
    return jsonify({'stock_data': stock_data})

@app.route('/api/stock-data/<symbol>')
def company_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='5d')
        data = {
            'latest_price': round(hist['Close'].iloc[-1], 2),
            'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            'closing_prices': hist['Close'].tolist(),
            'volumes': hist['Volume'].tolist()
        }
        return jsonify(data)
    except Exception:
        return jsonify({"error": f"No data available for symbol '{symbol}'"}), 404

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Logic to handle password reset (e.g., sending email with reset link)
        flash('If this email is registered, you will receive a password reset link.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


if __name__ == '__main__':
    app.run(debug=True)