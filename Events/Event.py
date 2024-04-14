class Event:
    def __init__(self, nom, categorie, place_dispo, date, prix, artiste):
        self.__nom = nom
        self.__categorie = categorie
        self.__place_dispo = place_dispo
        self.__date = date
        self.__prix = prix
        self.__artiste = artiste
    
    # Getters and Setters
    @property
    def nom(self):
        return self.__nom
    @nom.setter
    def nom(self, v):
        self.__nom = v

    @property
    def categorie(self):
        return self.__categorie
    @categorie.setter
    def categorie(self, v):
        self.__categorie = v

    @property
    def place_dispo(self):
        return self.__place_dispo
    @place_dispo.setter
    def place_dispo(self, v):
        self.__place_dispo = v

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, v):
        self.__date = v

    @property
    def prix(self):
        return self.__prix
    @prix.setter
    def prix(self, v):
        self.__prix = v
    
    @property
    def artiste(self):
        return self.__artiste
    @artiste.setter
    def artiste(self, v):
        self.__artiste = v
    
    