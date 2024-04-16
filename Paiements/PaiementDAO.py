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
        
