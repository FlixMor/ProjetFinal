class Reservation:
    def __init__(self, username, event, place, statut):
        self.__username = username
        self.__event = event
        self.__place = place
        self.__statut = statut

    # Getters and Setters
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, v):
        self.__id = v

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, v):
        self.__username = v

    @property
    def event(self):
        return self.__event
    @event.setter
    def event(self, v):
        self.__event = v

    @property
    def place(self):
        return self.__place
    @place.setter
    def place(self, v):
        self.__place = v

    @property
    def statut(self):
        return self.__statut
    @statut.setter
    def statut(self, v):
        self.__statut = v