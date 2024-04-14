class Paiement:
    def __init__(self, username, num_carte, num_secu):
        self.__username = username
        self.__num_carte = num_carte
        self.__num_secu = num_secu

    # Getters and Setters

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, v):
        self.__username = v

    @property
    def num_carte(self):
        return self.__num_carte
    @num_carte.setter
    def num_carte(self, v):
        self.__num_carte = v

    @property
    def num_secu(self):
        return self.__num_secu
    @num_secu.setter
    def num_secu(self, v):
        self.__num_secu = v