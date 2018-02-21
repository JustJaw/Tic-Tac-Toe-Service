import falcon
from pymongo import MongoClient
import smtplib

KEY = "abracadabra"
FROM = 'JustinandTed@python.com'
SUBJECT = "Hello!"
TEXT = "This message was sent with Python's smtplib."

def sendMail(user):

    toUser = [user['email']]  # must be a list

    # Prepare actual message
    message = "This is your key\n\tKEY : " + KEY

    # Send the mail
    server = smtplib.SMTP('localhost')
    server.sendmail(FROM, toUser, message)
    server.quit()

class addUser:
    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['winner'] = " "
        user['grid'] = [" "," "," "," "," "," "," "," "]

        sendMail(user)

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
    
