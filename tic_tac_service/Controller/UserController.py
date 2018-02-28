import falcon
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import smtplib
import Controller.MailController as MailResource
from bson import json_util, ObjectId
import Controller.GameController as Game
import dbmongo as DB
# from falcon_cors import CORS

#Global key for grading script
KEY = "abracadabra"
SERVER_VERIFY = 'http://130.245.171.42/verify/'
EMAIL_SUBJECT = 'Verify Your Email'


# Creates a new user
class addUser:
    #Used to not check for cookies
    no_auth = True
 
    def on_post(self, req, resp):

        user = req.media

        # Used for email message
        email_in_url_param = user['email'].replace(".", "||") + "/"

        user['enabled'] = False
        user['human'] = 0
        user['wopr'] = 0
        user['tie'] = 0
        user_id = DB.users.insert_one(user).inserted_id


        #Sends email
        email_message = "This is your key\n\tKEY : " + KEY + "\n"
        email_message += "OR\nClick Below\n"
        email_message += "\n" + SERVER_VERIFY + email_in_url_param + KEY
        MailResource.sendMail(user['email'], EMAIL_SUBJECT, email_message)

        Game.create_new_game(user_id)

        resp.media = {"status": "OK"}
        return


class verifyUser:
    no_auth = True

    def on_get(self, req, resp, email, key):
        email = email.replace("||", ".")

        if(self.able_to_verify(email, key) == True):
            resp.media = {"status": "OK"}
        else:
            resp.media = {"status": "ERROR", "message": "Incorrect Email"}

    def on_post(self, req, resp):
        userEmail = req.media['email']
        userKey = req.media['key']

        if(self.able_to_verify(userEmail, userKey) == True):
            resp.media = {"status": "OK"}
        else:
            resp.media = {"status": "ERROR", "message": "Incorrect Email"}

    def able_to_verify(self, userEmail, userKey):
            userFromDB = DB.users.find_one({"email": userEmail})

            if userFromDB is None or userKey != KEY:
                return False

            user_enabled = {"enabled": True}
            userFromDB = DB.users.find_one_and_update({'_id': userFromDB['_id']}, {
                "$set": user_enabled}, return_document=ReturnDocument.AFTER)

            return True


class cookieTest:
    def on_get(self, req, resp):
        resp.media = {"cookie": "req.cookies['theCookie']"}

    

class login:
    no_auth = True
    def on_post(self, req, resp):
        user=req.media

        Temp_username = user['username']
        Temp_password = user['password']
  
        userFromDB = DB.users.find_one({"username":  Temp_username})

        if userFromDB is not None and userFromDB['password'] == Temp_password:
            if(userFromDB['enabled'] is False):
                resp.media = {"status": "ERROR",
                              "message": "Must verify account"}
                              
            else:
                Temp_id = str(userFromDB['_id'])
                resp.set_cookie('theCookie', Temp_id)
                resp.media = {"status": "OK"}

        else:
            resp.media = {"status": "ERROR", "message": "Wrong username/password sorry"}


class logout:
    no_auth = True
    def on_post(self, req, resp):
        resp.unset_cookie('theCookie')
