from Users.User import User
import database

class UserDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    @classmethod
    def add(cls, user: User):
        sql = "INSERT INTO user (nom_complet, courriel, username, password, age, phone, usertype) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        params = (user.nom_complet, user.courriel, user.username, user.password, user.age, user.phone, user.usertype)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
    
    @classmethod # # Utilisé dans le app.py/login pour vérifier si l'utilisateur existe
    def get_user_by_username(cls, username):
        sql = "SELECT * FROM user WHERE username = %s"
        try:
            cls.cursor.execute(sql, (username,))
            user:User = cls.cursor.fetchone()
            message = "success"
            return (message, user)
        except Exception as error:
            user = None
            message = "failure"
            return (message, user) 

    # UPDATE NOM_COMPLET    entres = objet User , new_nom_complet 
    @classmethod
    def update_nom_complet(cls,user:User,new_nom_complet):
        sql = "UPDATE user SET nom_complet = %s WHERE nom_complet = %s"
        params = (new_nom_complet,user.nom_complet)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE COURRIEL    entres = objet User , new_courriel 
    @classmethod
    def update_courriel(cls,user:User,new_courriel):
        sql = "UPDATE user SET courriel = %s WHERE courriel = %s"
        params = (new_courriel,user.courriel)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE USERNAME    entres = objet User , new_username
    @classmethod
    def update_username(cls,user:User,new_username):
        sql = "UPDATE user SET username = %s WHERE username = %s"
        params = (new_username,user.username)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE password    entres = objet User , new_password
    @classmethod
    def update_password(cls,user:User,new_password):
        sql = "UPDATE user SET password = %s WHERE password = %s"
        params = (new_password,user.password)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE age    entres = objet User , new_age
    @classmethod
    def update_age(cls,user:User,new_age):
        sql = "UPDATE user SET age = %s WHERE age = %s"
        params = (new_age,user.age)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
    
    # UPDATE phone    entres = objet User , new_phone
    @classmethod
    def update_phone(cls,user:User,new_phone):
        sql = "UPDATE user SET phone = %s WHERE phone = %s"
        params = (new_phone,user.phone)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message