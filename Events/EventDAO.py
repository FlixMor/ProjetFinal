import database
from Events.Event import Event


class EventDAO:
    connexion = database.connexion_db()
    cursor = connexion.cursor()

    @classmethod
    def add(cls, event:Event):
        sql = "INSERT INTO event (nom, categorie, place_dispo, date, prix, artiste) VALUES(%s, %s, %s, %s, %s, %s)"
        params = (event.nom, event.categorie, event.place_dispo, event.date, event.prix, event.artiste)
        try:
            cls.cursor.execute(sql, params)
            cls.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    @classmethod
    def del_event(cls, nom):
        sql = "DELETE FROM event WHERE nom =%s"
        try:
            message = EventDAO.get_event_by_name(nom)
            EventDAO.cursor.execute(sql, (nom,))
            EventDAO.connexion.commit()
            return message
        except ValueError as error:
            return message == "failure"

        
    @classmethod 
    def get_event_by_name(cls, nom):
        sql = "SELECT * FROM event WHERE nom = %s"
        try:
            cls.cursor.execute(sql, (nom,))
            event:Event = cls.cursor.fetchone()
            message = "success"
            return (message, event)
        except Exception as error:
            event = None
            message = "failure"
            return (message, event)
        
    @classmethod
    def list_event(cls):
        events = []
        sql = "SELECT * FROM event"
        try:
            EventDAO.cursor.execute(sql)
            event_list = EventDAO.cursor.fetchall()
            message = "success"
        except Exception as error:
            event_list = []
            message = "failure"
        for event in event_list:
            nom , categorie , place_dispo , date, prix, artiste = event
            events.append({"nom":nom,"categorie":categorie,"place_dispo":place_dispo, "date":date, "prix":prix, "artiste":artiste})
        return (message,events)

    # UPDATE NOM    
    @classmethod
    def update_nom(cls,event:Event,new_nom):
        sql = "UPDATE event SET nom = %s WHERE nom = %s"
        params = (new_nom,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE CATEGORIE
    @classmethod
    def update_categorie(cls,event:Event,new_categorie):
        sql = "UPDATE event SET categorie = %s WHERE nom = %s"
        params = (new_categorie,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE PLACE_DISPO
    @classmethod
    def update_place_dispo(cls,event:Event,new_place_dispo):
        sql = "UPDATE event SET place_dispo = %s WHERE nom = %s"
        params = (new_place_dispo,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE DATE
    @classmethod
    def update_date(cls,event:Event,new_date):
        sql = "UPDATE event SET date = %s WHERE nom = %s"
        params = (new_date,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
        
    # UPDATE PRIX
    @classmethod
    def update_prix(cls,event:Event,new_prix):
        sql = "UPDATE event SET prix = %s WHERE nom = %s"
        params = (new_prix,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message
    
    # UPDATE phone    entres = objet User , new_phone
    @classmethod
    def update_artiste(cls,event:Event,new_artiste):
        sql = "UPDATE event SET artiste = %s WHERE nom = %s"
        params = (new_artiste,event.nom)
        try:
            EventDAO.cursor.execute(sql,params)
            EventDAO.connexion.commit()
            message = "success"
            return message
        except Exception as error:
            message = "failure"
            return message