from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt

from Users.User import User
from Users.UserDAO import UserDAO
from Events.Event import Event
from Events.EventDAO import EventDAO 

import re                       # Pour le phone pattern
from dotenv import load_dotenv  # Pour lire le fichier .env
import os                       # Pour lire le fichier .env
import database as db

# # # INITIALISATION # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
load_dotenv() # Chargement des variables d'environnement du fichier .env

phone_pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
salt = (bcrypt.gensalt(rounds = 12))


# CONTEXT PROCESSOR #
@app.context_processor
def inject_is_admin():
    def is_admin(username):
        return UserDAO.is_admin(username)
    return dict(is_admin=is_admin)

# # # HOME # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/')
def index():
    if "username" in session:
        return render_template('index.html', username=session["username"])
    else:
        return render_template("index.html")

# # # ABOUT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/about')
def about():
    if "username" in session:
        return render_template('about.html', username=session["username"])
    else:
        return render_template("about.html")
    
# # # REGISTER # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@app.route('/register', methods=["GET", "POST"])
def register():
    message="info"

    if "username" in session:
        return redirect(url_for("logout"))
    
    if request.method == "POST":
        req = request.form
        nom_complet = req['fullname']
        courriel = req['email']
        username = req['username']
        password = req['password']
        age = req['age']
        phone = req['phone']
        usertype = "basic"

        # Validation des entrées #
        if nom_complet=="" or courriel=="" or username=="" or password=="" or age=="" or phone=="":
            return render_template('register.html', message='empty')
        if (5 > len(nom_complet) or len(nom_complet) > 20):
            return render_template('register.html', message='invalidname')
        if (3 > len(username) or len(username) > 20):
            return render_template('register.html', message='invalidusername')
        if (10 > len(courriel) or len(courriel) > 30 or not email_pattern.match(courriel)):
            return render_template('register.html', message='invalidemail')            
        if (not 18 <= int(age) <= 100 or not age.isdigit()):
            return render_template('register.html', message='invalidage')
        if (not phone_pattern.match(phone)):
            return render_template('register.html', message='invalidphone')
        if not UserDAO.valid_password(password):
            return render_template('register.html', message='invalidpassword')
        
        else:  # Ajout du compte #  
            passwordbyte = password.encode('utf-8')
            password = bcrypt.hashpw(passwordbyte, salt)
            user = User(nom_complet, courriel, username, password, age, phone, usertype)
            message = UserDAO.add(user)
    return render_template('register.html', message=message)


# # # LOGIN # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash = UserDAO.get_password_by_user(username)

        if hash is not None: # Fonction get_password retourne soit le hash, soit "None" #
            hash = hash.encode('utf-8')
            passwordbyte = password.encode('utf-8')
            if bcrypt.checkpw(passwordbyte, hash):                       #
                session["username"] = username                           # User authenticated successfully
                return render_template("index.html", username=username)  #
            else:
                message = "invalidUsernamePassword" # Mauvais mot de passe
        else:
            message = "invalidUsernamePassword"     # Mauvais nom d'utilisateur
        return render_template("login.html", message=message) 
    else:
        message = "info"  # Si la requête est GET
        return render_template("login.html", message=message)

# # # LOGOUT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


# # # ACCOUNT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@app.route('/account', methods=['GET'])
def account():
    if "username" in session:
        message, user_data = UserDAO.get_user_by_username(session["username"])
        if message == "success":
            return render_template('account.html', username=session["username"], user=user_data)
        else:
            return render_template('error.html', message=message)  # Pass the error message from UserDAO
    else:
        return redirect(url_for("login"))
    
# # # EDIT-ACCOUNT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/edit-account', methods=['GET', 'POST'])
def edit_account():
    if "username" in session:

        message, user_data = UserDAO.get_user_by_username(session["username"])
        if message == "success":
            if request.method == 'POST':
                new_name = request.form.get('nom_complet', user_data.nom_complet)  
                new_username = request.form.get('username', user_data.username)
                new_email = request.form.get('courriel', user_data.courriel)
                new_phone = request.form.get('phone', user_data.phone)
                new_age = request.form.get('age', user_data.age)

                # Validation des entrées # 
                if new_name != user_data.nom_complet and (5 > len(new_name) or len(new_name) > 20):
                    return render_template('edit-account.html', message='invalidname', user=user_data)
                if new_username != user_data.username and (3 > len(new_username) or len(new_username) > 20):
                    return render_template('edit-account.html', message='invalidusername', user=user_data)
                if new_email != user_data.courriel and (10 > len(new_email) or len(new_email) > 30 or not email_pattern.match(new_email)):
                    return render_template('edit-account.html', message='invalidemail', user=user_data)  
                if new_phone != user_data.phone and (not phone_pattern.match(new_phone)):
                    return render_template('edit-account.html', message='invalidphone', user=user_data)    
                if new_age != user_data.age and (not 18 <= int(new_age) <= 100 or not new_age.isdigit()):
                    return render_template('edit-account.html', message='invalidage', user=user_data)
                
                # Si les entrées sont valides
                try:
                    if new_name != user_data.nom_complet:
                        UserDAO.update_nom_complet(user_data, new_name)   
                    if new_email != user_data.courriel:
                        UserDAO.update_courriel(user_data, new_email) 
                    if new_phone != user_data.phone:
                        UserDAO.update_phone(user_data, new_phone) 
                    if new_age != user_data.age:
                        UserDAO.update_age(user_data, new_age)
                    if new_username != user_data.username:
                        session["username"] = new_username
                        UserDAO.update_username(user_data, new_username) 
                    return redirect(url_for('account'))
                # Erreur lors de la mise a jour de la base de donnée #
                except Exception as error:
                    print(error)
                    message = "failure"
                    return render_template('edit-account.html', message=message, user=user_data)
                                
            else: # Requête GET
                message = "info" 
                return render_template('edit-account.html', message=message, user=user_data)
        else:
            return redirect(url_for("logout"))
    else:
        return redirect(url_for("login"))
    

# # # DELETE-ACCOUNT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/delete-account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']
        message, user = UserDAO.get_user_by_username(username)
        if message == "success" and not UserDAO.is_admin(username):
            message = UserDAO.delete_user(user)
            if message == "success":
                session.pop('username')
                return redirect(url_for('index')) 
            else:
                return render_template('error.html', message="deleteFailure") 
        else:
            return render_template('error.html', message="userNotFound") 
    else:
        return redirect(url_for('login'))

# # # EVENTS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@app.route('/events', methods=['GET'])
def events():
    if 'username' in session:
        # Récupération des events
        message, events = EventDAO.list_event()
        return render_template('events.html', username=session["username"], event=events)
    else:
        return redirect(url_for('login'))
    
# # # ADMIN PANEL # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@app.route('/admin-panel', methods=['GET','POST'])
def admin_panel():
    if 'username' in session:
        username = session["username"]
        if UserDAO.is_admin(username):
            if request.method == 'POST':
                req = request.form
                eventname = req['eventname']
                category = req['category']
                place_dispo = req['place_dispo']
                date = req['date']
                price = req['price']
                artist = req['artist']

                # Validation des entrées
                if (5 > len(eventname) or len(eventname) > 30):
                    return render_template('admin-panel.html', message='invalideventname')
                if (4 > len(category) or len(category) > 20):
                    return render_template('admin-panel.html', message='invalidcategory')
                if not (1 <= int(place_dispo) <= 999):
                    return render_template('admin-panel.html', message='invalidplacedispo')
                if (not date_pattern.match(date)):
                    return render_template('admin-panel.html', message='invaliddate')
                if not (1 <= int(price) <= 9999):
                    return render_template('admin-panel.html', message='invalidprice')
                if (4 > len(artist) or len(artist) > 25):
                    return render_template('admin-panel.html', message='invalidartist')
                # Si les entrées sont valides:
                try:
                    event = Event(eventname, category, place_dispo, date, price, artist)
                    message = EventDAO.add(event)
                    return render_template('admin-panel.html', username=username, message=message)
                except Exception as error:
                    print(error)
                    return render_template('admin-panel.html', username=username, message=message) 

            else:
                message = "info"
                return render_template('admin-panel.html', username=username, message=message)
        else:
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('logout'))

    
