from flask import Flask, render_template, request, redirect, url_for, session
#from flask_bcrypt import Bcrypt  # Utilisé pour le hashage des mots de passes #
import bcrypt
from Users.User import User
from Users.UserDAO import UserDAO

import re # Pour le phone pattern

from dotenv import load_dotenv # Pour lire le fichier .env
import os                      # Pour lire le fichier .env

import database as db

load_dotenv() # Chargement des variables d'environnement du fichier .env


# # # INITIALISATION # # #

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
#bcrypt = Bcrypt(app)  

phone_pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
salt = (bcrypt.gensalt(rounds = 12))

# # # HOME # # #
@app.route('/')
def index():
    if "username" in session:
        return render_template('index.html', username=session["username"])
    else:
        return render_template("index.html")

# # # ABOUT # # #
@app.route('/about')
def about():
    if "username" in session:
        return render_template('about.html', username=session["username"])
    else:
        return render_template("about.html")

# # # LOGIN # # #
@app.route('/login', methods=["GET", "POST"])
def login():
    # Check if the user is already logged in
    if "username" in session:
        return redirect(url_for("logout"))

    if request.method == "POST":
        req = request.form
        username = request.form["username"]
        password = request.form["password"]
        message, user = UserDAO.get_user_by_username(username)
        hash = UserDAO.get_password_by_user(username)
        hash = hash.encode('utf-8')
        passwordbyte = password.encode('utf-8')

        if bcrypt.checkpw(passwordbyte, hash):
            # User authenticated successfully
            session["username"] = username
            return render_template("index.html", username=username)
        else:
            message = "Invalid username or password"

        return render_template("login.html", message=message)
    else:
        message = "info"
        return render_template("login.html", message=message)

# # # LOGOUT # # #
@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

# # # ACCOUNT # # #
@app.route('/account')
def account():
    if "username" in session:
        return render_template('account.html', username=session["username"])
    else:
        return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    # Check if the user is already logged in
    if "username" in session:
        return redirect(url_for("logout"))

    message = ""
    user = None
    
    if request.method == "POST":
        req = request.form
        nom_complet = req['fullname']
        courriel = req['email']
        username = req['username']
        password = req['password']
        #password = bcrypt.generate_password_hash((req['password']).encode('utf-8'))
        #salt = bcrypt.gensalt(rounds=12)
        #password = bcrypt.hashpw(password, salt)

        #bcrypt.
        age = req['age']
        phone = req['phone']
        usertype = "basic"

        
        if nom_complet=="" or courriel=="" or username=="" or password=="" or age=="" or phone=="":
            message = "failure"

        elif not (18 <= int(age) <= 100):
            message = 'invalidage'
            return render_template('register.html', message=message)
        
        elif not phone_pattern.match(phone):
            message = 'invalidphone'
            return render_template('register.html', message=message)
        
        else:    
            passwordbyte = password.encode('utf-8')
            password = bcrypt.hashpw(passwordbyte, salt)
            user = User(nom_complet, courriel, username, password, age, phone, usertype)
            message = UserDAO.add(user)
    else:
        message ="info"
            
    return render_template('register.html', message=message, user=user)




# python -m flask --app app run --debug #
