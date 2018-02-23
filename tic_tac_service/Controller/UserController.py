import falcon
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import smtplib
import Controller.MailController as MailResource
from bson import json_util, ObjectId
import GameController as Game

KEY = "abracadabra"


client = MongoClient()
db = client['tic-tac-toe']
usersCollection = db['users']


class addUser:
    no_auth = True

    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['human'] = 0
        user['wopr'] = 0
        user['tie'] = 0

        currentGame = {}
        currentGame['move'] = Game.EMPTY_SPACE
        currentGame['winner'] = Game.NO_WINNER_YET
        currentGame['grid'] = Game.EMPTY_GRID

        user['current_game'] = currentGame

        email_message = "This is your key\n\tKEY : " + KEY

        #MailResource.sendMail(user['email'], email_message)

        usersCollection.insert(user)

        resp.body = json_util.dumps(user)
        return


class verifyUser:
    no_auth = True

    def on_post(self, req, resp):
        user = req.media
        userEmail = user['email']

        userFromDB = usersCollection.find_one({"email": userEmail})

        if userFromDB is None:
            resp.media = {"error": "Wrong Email"}
            return
        else:
            if user['key'] != KEY:
                raise falcon.HTTPBadRequest(
                    'KEY',
                    'Incorrect key')

            user_enabled = {"enabled": True}
            userFromDB = usersCollection.find_one_and_update({'_id': userFromDB['_id']}, {
                "$set": user_enabled}, return_document=ReturnDocument.AFTER)

            print(userFromDB)
            resp.media = {"success": "You have been verified"}
            return


class cookieTest:
    def on_get(self, req, resp):
        resp.body = req.cookies['cookie']

    

class login:
    no_auth = True



    def on_post(self, req, resp):


        user=req.media


        Temp_username = user['username']
        Temp_password = user['password']
  

        userFromDB = usersCollection.find_one({"username":  Temp_username})
         
      

        if userFromDB is not None and userFromDB['password'] == Temp_password:

            Temp_id = str(userFromDB['_id'])



            resp.set_cookie('theCookie', Temp_id)



        else:
             resp.body="Wrong username/password sorry"




class logout:
    no_auth = True
    def on_post(self, req, resp):
      
        resp.unset_cookie('theCookie')
