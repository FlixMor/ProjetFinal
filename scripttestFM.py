from Reservations.Reservation import Reservation
from Reservations.ReservationDAO import ReservationDAO

from Users.UserDAO import UserDAO
from Users.User import User
from Events.EventDAO import EventDAO
from Events.Event import Event
from Paiements.Paiement import Paiement
from Paiements.PaiementDAO import PaiementDAO

message, user = UserDAO.get_user_by_username('flixu')
message2, event = EventDAO.get_event_by_name('Soiree douce')
#events = Event('Tester','Humor',75,'2025-01-01','56$','Martine')
#messages = EventDAO.add(events)
#carte = Paiement('allo','454548644896','45868')
#EventDAO.update_place_dispo(event,50)
#print(user,event)
#message = ReservationDAO.add(user,event,15)
#reservations = ReservationDAO.get_reservation_by_user(user)
#message = ReservationDAO.del_reservation(user,event)
#message =PaiementDAO.cancel_pay(user,event)
#message = PaiementDAO.add(user,carte)
#message = PaiementDAO.pay(user,event)
#message = PaiementDAO.del_pay(user)
#message = PaiementDAO.get_pay_by_user(user)
