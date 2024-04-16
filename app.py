from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from Users.User import User
from Users.UserDAO import UserDAO
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
salt = (bcrypt.gensalt(rounds = 12))

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
    return render_template('register.html', message=message)


# # # LOGIN # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash = UserDAO.get_password_by_user(username)

        if hash is not None:
            hash = hash.encode('utf-8')
            passwordbyte = password.encode('utf-8')
            if bcrypt.checkpw(passwordbyte, hash):                       #
                session["username"] = username                           # User authenticated successfully
                return render_template("index.html", username=username)  #
            else:
                message = "invalidUsernamePassword"
        else:
            message = "invalidUsernamePassword"
        return render_template("login.html", message=message) 
    else:
        message = "info"
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
                new_name = request.form['nom_complet']  
                new_username = request.form['username']
                new_email = request.form['courriel']
                new_phone = request.form['phone']
                new_age = request.form['age']

                if new_name != user_data.nom_complet:
                    if 5 <= len(new_name) <= 20  and new_name is not None:
                        pass    
                    else:
                        message = 'invalidname'
                        return render_template('edit-account.html', message=message, user=user_data)

                elif new_username != user_data.username:
                    if 3 <= len(new_username) <= 20  and new_username is not None:
                        pass 
                    else:
                        message = 'invalidusername'
                        return render_template('edit-account.html', message=message, user=user_data)

                elif new_email != user_data.courriel:
                    if 5 <= len(new_email) <= 30 and email_pattern.match(new_email) and new_email is not None:
                        pass    
                    else:
                        message = 'invalidemail'
                        return render_template('edit-account.html', message=message, user=user_data)
                    
                elif new_phone != user_data.phone:
                    if phone_pattern.match(new_phone) and new_phone is not None:
                        pass    
                    else:
                        message = 'invalidphone'
                        return render_template('edit-account.html', message=message, user=user_data)
                    
                elif new_age != user_data.age:
                    if (18 <= int(new_age) <= 100) and new_age.isdigit() and new_age is not 0:
                        pass
                    else:
                        message = 'invalidage'
                        return render_template('edit-account.html', message=message, user=user_data)
                                        
                try:
                    UserDAO.update_nom_complet(user_data, new_name)   
                    UserDAO.update_courriel(user_data, new_email) 
                    UserDAO.update_phone(user_data, new_phone) 
                    UserDAO.update_age(user_data, new_age)
                    session["username"] = new_username
                    UserDAO.update_username(user_data, new_username) 
                    return redirect(url_for('account'))
                except Exception as error:
                    print(error)
                    message = "failure"
                    return render_template('edit-account.html', message=message, user=user_data)                            
            # For GET request or failed POST request, render the template   
            else:
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
        if message == "success":
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
    

    
