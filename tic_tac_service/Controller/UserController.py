import falcon
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import smtplib
import Controller.MailController as MailResource
from bson import json_util, ObjectId
import Controller.GameController as Game
import dbmongo as DB

KEY = "abracadabra"


class addUser:
    no_auth = True

    def on_post(self, req, resp):

        #Creates new user
        user = req.media
        user['enabled'] = False
        user['human'] = 0
        user['wopr'] = 0
        user['tie'] = 0
        user_id = DB.users.insert_one(user).inserted_id

        #Sends email
        email_message = "This is your key\n\tKEY : " + KEY
        #MailResource.sendMail(user['email'], email_message)
        

        Game.create_new_game(user_id)

        resp.media = {"status": "OK"}
        return


class verifyUser:
    no_auth = True

    def on_post(self, req, resp):
        user = req.media
        userEmail = user['email']

        userFromDB = DB.users.find_one({"email": userEmail})

        if userFromDB is None:
            resp.media = {"status": "error", "message": "Wrong Email"}
            return
        else:
            if user['key'] != KEY:
                raise falcon.HTTPBadRequest(
                    'KEY',
                    'Incorrect key')

            user_enabled = {"enabled": True}
            userFromDB = DB.users.find_one_and_update({'_id': userFromDB['_id']}, {
                "$set": user_enabled}, return_document=ReturnDocument.AFTER)

            print(userFromDB)
            resp.media = {"status": "OK"}
            return


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
