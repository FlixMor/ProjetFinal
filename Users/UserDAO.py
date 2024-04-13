from Users.User import User
import database

class UserDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    @classmethod
    def add(cls,user:User):
        sql = "INSERT INTO user(nom_complet,courriel,username,password) VALUE (%s,%s,%s,%s)"
        params = (user.nom_complet,user.courriel,user.username,user.password)
        try:
            UserDAO.cursor.execute(sql,params)
            UserDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message