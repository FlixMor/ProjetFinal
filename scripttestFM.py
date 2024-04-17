from Reservations.Reservation import Reservation
from Reservations.ReservationDAO import ReservationDAO

from Users.UserDAO import UserDAO
from Users.User import User
from Events.EventDAO import EventDAO
from Events.Event import Event
import database

message, user = UserDAO.get_user_by_username('allo')
message2, event = EventDAO.get_event_by_name('Evenement')
message3 = ReservationDAO.add(user,event,15)
reservations = ReservationDAO.get_reservation_by_user(user)
#ReservationDAO.del_reservation(user,event)