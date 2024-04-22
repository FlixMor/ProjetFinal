from Paiements.Paiement import Paiement
from Users.User import User
from Events.Event import Event
import database

class PaiementDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    @classmethod
    def add(cls,user:User, paiement:Paiement):
        sql = "INSERT INTO paiement (username, num_carte, num_secu) VALUES(%s, %s, %s)"
        print(user)
        params = (user.username, paiement.num_carte, paiement.num_secu)
        
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
    
    @classmethod
    def pay(cls,user:User,event:Event):
        sql = "UPDATE reservation SET statut = 'paid' WHERE username =%s and event =%s"
        params = (user.username,event.nom)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()

            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    @classmethod
    def cancel_pay(cls,user:User,event:Event):
        sql = "UPDATE reservation SET statut = 'unpaid' WHERE username =%s and event =%s"
        params = (user.username,event.nom)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message

    @classmethod    
    def del_pay(cls,user:User):
        sql = "DELETE FROM paiement where username = %s"
        print(user.username)
        params = (user.username,)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    @classmethod 
    def get_pay_by_user(cls,user:User):
        sql = "SELECT * FROM paiement where username = %s"
        params = (user.username,)
        try:
            cls.cursor.execute(sql, params)
            data = cls.cursor.fetchall()
            return data
        except Exception as error:
            return None