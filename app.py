from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db') # Connects the app to the database
app.config['SECRET_KEY'] = "mysecretkey"
db = SQLAlchemy(app) # Create the database instance
# db.init_app(app) # Initialize the database instance


# The table for the user in the database
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database if it doesn't exist
        print("Database created!")
    app.run(debug=True)
