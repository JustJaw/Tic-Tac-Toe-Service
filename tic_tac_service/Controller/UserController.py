import falcon
import pymongo
import smtplib


class addUser:
    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False
        user['winner'] = " "
        user['grid'] = [" "," "," "," "," "," "," "," "]





FROM = 'JustinandTed@python.com'

TO = [user['email']] # must be a list

SUBJECT = "Hello!"

TEXT = "This message was sent with Python's smtplib."

# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail

server = smtplib.SMTP('myserver')
server.sendmail(FROM, TO, message)
server.quit()











        print(user)
        resp.media = user




class verifyUser:


def on_post(self, req, resp):
user = req.media
userEmail= user['email']

client= MongoClient()
db = client['tic-tac-toe']

collection= db['users']

from bson.bject import ObjectId

userFromDB= db.collection.find_one({'email': userEmail})

if(userFromDB=""){
	
	print("Wrong email")
}


else{
userFromDB['enabled'] = True
	

collection.update_one({'_id':userFromDB['_id']}, {"$set": post}, upsert=False)


resp.media =user
}
