from Reservations import Reservation
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
        sql = "INSERT INTO reservation (username, event, place, statut) VALUES (%s, %s, %s, %s)"
        params = (user.username, event.nom, seat,'unpaid')
        try:
            if seat > event.place_dispo:
                message = "failure place"
                return message
            else:
                cls.cursor.execute(sql, params)
                cls.connexion.commit()
                sql2 = "SELECT place_dispo from event WHERE nom =%s"
                cls.cursor.execute(sql2, (event.nom,))
                place_dispo = cls.cursor.fetchall()
                place_disp = place_dispo[0]

            if place_disp[0]-seat <= 0:
                message = "failure place"
                return message
            else:
                sql3 = "UPDATE event SET place_dispo =%s WHERE nom =%s"
                place_restante = place_disp[0] - seat
                params2 = (place_restante,event.nom)
                cls.cursor.execute(sql3,params2)
                cls.connexion.commit()
                message = "success"
                return message
        except Exception as error:
            message = "failure tout court"
            return message
        

    @classmethod
    def del_reservation(cls,user:User,event:Event):

        sql = "SELECT place FROM reservation WHERE username = %s AND event =%s"
        params = (user.username,event.nom)
        try:
            cls.cursor.execute(sql, params)
            place_prise = cls.cursor.fetchall()
        except ValueError as error:
            message = "failure"
            return message
        sql2 = "DELETE FROM reservation WHERE username =%s AND event =%s"
        try:
            cls.cursor.execute(sql2, params)
            cls.connexion.commit()
        except ValueError as error:
            message = "failure"
            return message
        try:
            sql3 = "SELECT place_dispo FROM event WHERE nom=%s"
            cls.cursor.execute(sql3, (event.nom,))
            place_dispo = cls.cursor.fetchall()
            place_restante = place_dispo[0][0] + place_prise[0][0]
        except ValueError as error:
            message = "failure"
            return message
        try:
            sql4 = "UPDATE event SET place_dispo = %s WHERE nom=%s"
            params4 = (place_restante,event.nom)
            cls.cursor.execute(sql4, params4)
            cls.connexion.commit()
            message = "success"
            return message
        except ValueError as error:
            message = "failure"
            return message
        
    @classmethod
    def get_reservation_by_user(cls,user:User):
        sql = "SELECT * FROM reservation WHERE username =%s"
        try:
            params= (user.username,)
            cls.cursor.execute(sql, params)
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
        
    @classmethod
    def get_reservation_by_user_and_event(cls,user:User,event:Event):
        sql = "SELECT * FROM reservation WHERE username =%s AND event =%s"
        try:
            params= (user.username,event.nom)
            cls.cursor.execute(sql, params)
            result = cls.cursor.fetchall()
            return result
        except ValueError as error:
            return None