import falcon
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
import smtplib
import Controller.MailController as MailResource
from bson import json_util, ObjectId

KEY = "abracadabra"


client = MongoClient()
db = client['tic-tac-toe']
usersCollection = db['users']


class addUser:
    no_auth = True

    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['winner'] = " "
        user['grid'] = [" ", " ", " ", " ", " ", " ", " ", " "]

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

        if userFromDB == "":    
            print("Wrong email")
        else:
            userFromDB['enabled'] = True
            collection.update_one({'_id': userFromDB['_id']}, {
                                  "$set": user_enabled}, upsert=False)
            resp.media =user


class cookieTest:
    def on_get(self, req, resp):
        resp.body = req.cookies['cookie']

    

