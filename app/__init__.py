from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Correctly URL-encoded password
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:T%21m3L1n3%40Secure%232024@localhost:5433/stock_market'

# Optional: Disable track modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

from app import routes

# Optional: Print to verify configuration
print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
