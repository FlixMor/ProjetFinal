from Reservation import Reservation
from Users.User import User
from Events.Event import Event
from Events.EventDAO import EventDAO
import database

class ReservationDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    #---------------------------------------------------#
    #   Pour changer le statut de reservation a paid,   #
    #   il faut utiliser la methode PaiementDAO.pay()   #
    #---------------------------------------------------#

    @classmethod
    def add(cls,user:User,event:Event,seat):
        sql = "INSERT INTO reservation (username, event, place, statut) VALUES(%s, %s, %s, %s)"
        params = (user.username, event.nom, seat,'unpaid')
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            sql = "SELECT place_dispo from event WHERE nom =%s"
            cls.cursor.execute(sql, (event.nom,))
            place_dispo = cls.cursor.fetchone()
            if place_dispo[0] == 0:
                message = "failure"
                return message
            else:
                sql = "UPDATE event SET place_dispo =%s WHERE nom =%s"
                cls.cursor.execute(sql, (place_dispo[0]-1,event.nom))
                message = "success"
                return message
        except Exception as error:
            message = "failure"
            return message
        

    @classmethod
    def del_reservation(cls,user:User,event:Event):
        sql = "DELETE FROM reservation WHERE username =%s AND event =%s"
        try:
            message = EventDAO.get_event_by_name(user.username)
            EventDAO.cursor.execute(sql, (user.username,event.nom))
            EventDAO.connexion.commit()
            return message == "success"
        except ValueError as error:
            return message == "failure"
        
    @classmethod
    def get_reservation_by_user(cls,user:User):
        sql = "SELECT * FROM reservation WHERE username =%s"
        try:
            cls.cursor.execute(sql, (user.username,))
            result = cls.cursor.fetchall()
            return result
        except ValueError as error:
            return None
        
    @classmethod
    def get_reservation_by_event(cls,event:Event):
        sql = "SELECT * FROM reservation WHERE event =%s"
        try:
            cls.cursor.execute(sql, (event.nom,))
            result = cls.cursor.fetchall()
            return result
        except ValueError as error:
            return None
        