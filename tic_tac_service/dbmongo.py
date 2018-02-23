from pymongo import MongoClient

client = MongoClient()
db = client['tic-tac-toe']
users = db['users']
games = db['games']
