class User:
    def __init__(self, nom_complet, courriel, username, password) -> None:
        self.__nom_complet = nom_complet
        self.__courriel = courriel
        self.__username = username
        self.__password = password

    @property
    def nom_complet(self):
        return self.__nom_complet
    @nom_complet.setter
    def nom_complet(self, v):
        self.__nom_complet = v

    @property
    def courriel(self):
        return self.__courriel
    @courriel.setter
    def courriel(self, v):
        self.__courriel = v

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, v):
        self.__username = v

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, v):
        self.__password = v