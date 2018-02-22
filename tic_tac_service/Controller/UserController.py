import falcon
from pymongo import MongoClient
import smtplib
import Controller.MailController as MailResource

KEY = "abracadabra"


client = MongoClient()
db = client['tic-tac-toe']
collection = db['users']

class addUser:
    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['winner'] = " "
        user['grid'] = [" "," "," "," "," "," "," "," "]

        email_message = "This is your key\n\tKEY : " + KEY

        #MailResource.sendMail(user['email'], email_message)
        
        collection.insert(user, check_keys=False)

        resp.media = user

class verifyUser:
    def on_post(self, req, resp):
        user = req.media
        userEmail= user['email']

        userFromDB= db.collection.find_one({'email': userEmail})

        user_enabled = {"enabled": True}

        if userFromDB == "":    
            print("Wrong email")
        else:
            if user['key'] != KEY:
                raise falcon.HTTPBadRequest(
                    'KEY',
                    'Incorrect key')

            userFromDB['enabled'] = True
            collection.update_one({'_id': userFromDB['_id']}, {
                                  "$set": user_enabled}, upsert=False)
            resp.media =user
    
