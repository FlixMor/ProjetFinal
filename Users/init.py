import database
from User import User
from UserDAO import UserDAO
#
#hash = UserDAO.get_password_by_user('tony')
#print(hash)


import bcrypt
password = b"password123"
print(type(password))
salt = bcrypt.gensalt(rounds=15)
hashed_password = bcrypt.hashpw(password, salt)
if bcrypt.checkpw(password, hashed_password):
    print("Password is correct")
else:
    print("Password is incorrect")