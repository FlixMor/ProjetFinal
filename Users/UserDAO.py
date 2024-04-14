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
