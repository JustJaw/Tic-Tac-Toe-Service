import falcon
from pymongo import MongoClient
import smtplib
import MailController

KEY = "abracadabra"
FROM = 'JustinandTed@python.com'
SUBJECT = "Hello!"
TEXT = "This message was sent with Python's smtplib."

class addUser:
    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['winner'] = " "
        user['grid'] = [" "," "," "," "," "," "," "," "]

        email_message = "This is your key\n\tKEY : " + KEY

        MailController.sendMail(user['email'], email_message)

        print(user)
        resp.media = user

class verifyUser:
    def on_post(self, req, resp):
        user = req.media
        userEmail= user['email']

        client = MongoClient()
        db = client['tic-tac-toe']

        collection= db['users']

        userFromDB= db.collection.find_one({'email': userEmail})

        user_enabled = {"enabled": True}

        if userFromDB == "":    
            print("Wrong email")
        else:
            userFromDB['enabled'] = True
            collection.update_one({'_id': userFromDB['_id']}, {
                                  "$set": user_enabled}, upsert=False)
            resp.media =user
    
