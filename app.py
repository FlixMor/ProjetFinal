from flask import Flask, render_template, request, redirect, url_for, session

from Users.User import User
from Users.UserDAO import UserDAO


from dotenv import load_dotenv # Pour lire le fichier .env
import os                      # Pour lire le fichier .env

import database as db

load_dotenv() # Chargement des variables d'environnement du fichier .env


# # # INITIALISATION # # #

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        message, user = UserDAO.get_user_by_username(username)
        
        if message == "success":
            if user and user[4] == password:  # Assuming password is stored in the 5th column
                # User authenticated successfully
                session["username"] = username
                return redirect(url_for("index"))
            else:
                message = "Invalid username or password"
        else:
            message = "User not found"
        
        return render_template("login.html", message=message)
    else:
        return render_template("login.html")

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
    message = ""
    user = None
    
    if request.method == "POST":
        req = request.form
        nom_complet = req['nom_complet']
        courriel = req['courriel']
        username = req['username']
        password = req['password']
        age = req['age']
        phone = req['phone']
        usertype = "basic"

        if nom_complet=="" or courriel=="" or username=="" or password=="" or age=="" or phone=="":
            message = "error"
        else:    
            user = User(nom_complet, courriel, username, password, age, phone, usertype)
            message = UserDAO.add(user)
            
    return render_template('register.html', message=message, user=user)




# python -m flask --app app run --debug #
