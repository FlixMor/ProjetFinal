from Reservation import Reservation
from ReservationDAO import ReservationDAO
from Users.UserDAO import UserDAO
from Events.EventDAO import EventDAO
import database

message, user = UserDAO.get_user_by_username('allo')
message2, event = EventDAO.get_event_by_name('Evenement')

message3 = ReservationDAO.add(user,event,15)
message4, reservations = ReservationDAO.get_reservation_by_user('allo')

print(message)
print(message2)
print(message3)
print(message4)
print(reservations)