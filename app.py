import time
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from open_port_checker import is_port_available
import logging
import asyncio
from gevent.pywsgi import WSGIServer


logging.basicConfig(filename='app.log', level=logging.INFO)  # Configuração do log

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db') # Connects the app to the database
app.config['SECRET_KEY'] = "mysecretkey"
db = SQLAlchemy(app) # Create the database instance
# db.init_app(app) # Initialize the database instance

login_manager = LoginManager() # Allow the app and flask work together
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# The table for the user in the database
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username already exists! Please try another one.") 


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if not existing_user_username:
            raise ValidationError("Username does not exist!") 


@app.route('/')
def home():
    return render_template('home.html')


async def shutdown():
    loop = asyncio.get_event_loop()
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    loop.stop()


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown_request():
    print("Encerrando o servidor...")
    asyncio.run(shutdown())  # Chama a função shutdown de forma assíncrona
    return render_template('shutdown.html')


@app.route('/login', methods=['GET', 'POST']) 
def login():
    form = LoginForm()
    
    print("Login page")
    if form.validate_on_submit():
        print("Login attempt")
        # Check if the user exists
        # name = form.username.data.lower().strip()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("User exists")
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST']) 
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name = form.username.data.lower().strip()
        new_user = User(username=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_names = User.query.all()

    return render_template('dashboard.html', items=user_names)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    logging.info("Aplicativo iniciado")  # Loga a mensagem quando o aplicativo é iniciado
    
    port = None
    for port_i in range(5000, 8000):
        if is_port_available(port_i):
            port = port_i
            break
        else:
            continue

    if port:
        # Inicia o servidor Gevent na porta encontrada
        http_server = WSGIServer(('0.0.0.0', port), app)
        logging.info(f"Servidor Gevent iniciado na porta {port}")
        print("\n\n\n")
        print("##### VVHHHHHHHVV #####")
        print("#####   VVHHHVV   #####")
        print("#####     VHV     #####")
        print("#####      V      #####")
        print("\n")
        print(f"To open the app, go to:")
        print(f"localhost:{port}/")
        print("\n")
        print(f"Para abrir o aplicativo, acesse:")
        print(f"localhost:{port}/")
        http_server.serve_forever()
    else:
        logging.error("Nenhuma porta disponível para iniciar o servidor.")
