class User:
    def __init__(self, nom_complet, courriel, username, password, age, phone, usertype):
        self.__id = None
        self.__nom_complet = nom_complet
        self.__courriel = courriel
        self.__username = username
        self.__password = password
        self.__age = age
        self.__phone = phone
        self.__usertype = usertype
    
    # Getters and Setters
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, v):
        self.__id = v

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

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, v):
        self.__age = v
    
    @property
    def phone(self):
        return self.__phone
    @phone.setter
    def phone(self, v):
        self.__phone = v
    
    @property
    def usertype(self):
        return self.__usertype
    @usertype.setter
    def usertype(self, v):
        self.__usertype = v