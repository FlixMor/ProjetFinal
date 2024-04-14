from Paiements.Paiement import Paiement
import database

class PaiementDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    @classmethod
    def add(cls, paiement:Paiement):
        sql = "INSERT INTO paiement (username, num_carte, num_secu) VALUES(%s, %s, %s)"
        params = (paiement.username, paiement.num_carte, paiement.num_secu)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message