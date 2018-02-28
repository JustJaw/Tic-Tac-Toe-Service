# Module: GameController.py

import falcon
import dbmongo as DB
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson import json_util
from bson.objectid import ObjectId
import datetime
import pprint

CLIENT_PLAYER = 'X'
SERVER_PLAYER = 'O'
EMPTY_SPACE = ' '
NO_WINNER_YET = ' '
TIE_WINNER = ' '
GRID_SIZE = 9
VECTOR_SIZE = 3
EMPTY_GRID = [EMPTY_SPACE] * GRID_SIZE

last_move_index = 0


def create_new_game(user_id):

    #Creates a new game
    new_game = {}
    new_game['start_date'] = None
    new_game['finished'] = False
    new_game['user_id'] = ObjectId(user_id)
    new_game['id'] = None

    #Create gameplay board
    gameplay = {}
    gameplay['winner'] = NO_WINNER_YET
    gameplay['grid'] = EMPTY_GRID
    gameplay['move'] = None
    new_game['gameplay'] = gameplay

    #Inserts creates new game and sets id for the grading script
    new_game_id = DB.games.insert_one(new_game).inserted_id
    current_game_id = {}
    current_game_id['id'] = str(new_game_id)
    game = DB.games.find_one_and_update({'_id': new_game_id}, {
        "$set": current_game_id}, return_document=ReturnDocument.AFTER)

    return game


def get_win_vector(grid, player):
    if(grid.count(player) == VECTOR_SIZE):
        return player
    else:
        return NO_WINNER_YET


def determine_winner(grid, player):

    # Check Rows
    for i in range(0, VECTOR_SIZE):
        li = grid[i*VECTOR_SIZE: (i*VECTOR_SIZE) + VECTOR_SIZE]
        if(player == get_win_vector(li, player)):
            return player

    # Check Columns
    for i in range(0, VECTOR_SIZE):
        li = grid[i::VECTOR_SIZE]
        if(player == get_win_vector(li, player)):
            return player

    # Check Diagonals
    li1 = grid[0::VECTOR_SIZE+1]
    li2 = list(grid[VECTOR_SIZE - 1 :: VECTOR_SIZE - 1])[:-1]
    if(player == get_win_vector(li1, player) 
    or player == get_win_vector(li2, player)):
        return player
    
    return NO_WINNER_YET


def save_game(game):

    game_id = game['_id']
    gameplay = game['gameplay']

    if game['start_date'] is None:
        game['start_date'] = datetime.datetime.now()

    if not game['finished']:
        DB.games.update_one({'_id': game_id}, {
            "$set": game})
    else:
        finished_game = DB.games.find_one_and_update({'_id': game_id}, {
            "$set": game}, return_document=ReturnDocument.AFTER)

        the_winner = {}
        if gameplay['winner'] is CLIENT_PLAYER:
            the_winner["human"] = 1
        elif gameplay['winner'] is SERVER_PLAYER:
            the_winner["wopr"] = 1
        elif gameplay['winner'] is TIE_WINNER:
            the_winner["tie"] = 1

        user_id = finished_game['user_id']
        userFromDB = DB.users.find_one_and_update({'_id': user_id}, {
            "$inc": the_winner}, return_document=ReturnDocument.AFTER)
        
        # gameplay['grid'] = EMPTY_GRID

    return gameplay

# If the game does not exist and the user if verfied/enabled, then a game is created
def get_game_of_user(user_id):
    game = DB.games.find_one(
        {"user_id": ObjectId(user_id), "finished": False})

    if game is None:
        #Check if user is enabled and verified
        verified_user = DB.users.find_one(
            {"_id": ObjectId(user_id), "enabled": True})

        if(verified_user):
            game = create_new_game(user_id)
    return game
        
class PlayResource:
    def on_post(self, req, resp):
        
        # Client Move
        c_move = req.media['move'] 

        # Server Move
        move = None
        winner = NO_WINNER_YET
        
        user_id = str(req.cookies['theCookie'])
        game = get_game_of_user(user_id)

        if(game is None):
            resp.media = {"Status": "ERROR", "Message": "Not Verified"}
            return

        grid = game['gameplay']['grid']
        
        if c_move is not None and (c_move >= 0 and c_move < GRID_SIZE) and grid[c_move] is EMPTY_SPACE:
            grid[c_move] = CLIENT_PLAYER
            winner = determine_winner(grid, CLIENT_PLAYER)

            if(winner != CLIENT_PLAYER): 
                try:
                    move = grid.index(EMPTY_SPACE)
                    grid[move] = SERVER_PLAYER
                    winner = determine_winner(grid, SERVER_PLAYER)
                except ValueError: # If there are no empty spaces left
                    winner = TIE_WINNER
                    game['finished'] = True
            else:
                # Used to save the last move which is the user's winning move
                move = c_move

            if(winner is CLIENT_PLAYER or winner is SERVER_PLAYER):
               game['finished'] = True

            gameplay = {
                'grid': grid,
                'winner': winner,
                'move': move
            }

            game['gameplay'] = gameplay
            gameplay = save_game(game)
        

            # Clear grid and saves game if winner is decided
            # if (game['finished'] and winner is TIE_WINNER):
            #    gameplay['grid'] = EMPTY_GRID

        else:
            gameplay = game['gameplay']
            gameplay['move'] = move
            
        gameplay['status'] = "OK"
        resp.media = gameplay

class GamesResource:
    no_auth = True

    def on_get(self, req, resp):
        games = DB.games.find()
        resp.body = json_util.dumps(games)

class GameBoard:
    def on_get(self, req, resp):
        user_id = str(req.cookies['theCookie'])
        game = get_game_of_user(user_id)
        if game is None:
            resp.media = {"status": "ERROR", "Message": "Not Verified"}
        else:
            game_board = game['gameplay']
            resp.body = json_util.dumps(game_board)


class getscore:
    def on_get(self, req, resp):
        get_score(req, resp)

    def on_post(self,req,resp):
        get_score(req, resp)

    def get_score(self, req, resp):
        user_id = str(req.cookies['theCookie'])

        user = DB.users.find_one(
            {"_id": ObjectId(user_id), "enabled": True})

        if(user is None):
            resp.media = {"Status": "ERROR", "Message": "Not Verified"}
        else:
            score = {
                "status": "OK",
                "human": user['human'],
                "wopr": user['wopr'],
                "tie": user['tie']
            }

            resp.media = score

        

########### added by teddy onwards
class listgames:

    no_auth = True

    def on_get(self, req, resp):
        get_games()
        
    def on_post(self, req, resp):
        get_games()

    def get_games(self):
        started_games = {"start_date": {"$ne": None}}

        gamesDB = DB.games.find(started_games)

        games = {
            "status": "OK",
            "games": json_util.loads(json_util.dumps(gamesDB)),
        }

        resp.body = json_util.dumps(games)


class getgame:

    no_auth = True

    def on_post(self, req, resp):

        Tempgame=req.media

        gameID= Tempgame['id'] 
        
        gameFromDB = DB.games.find_one({"_id": ObjectId(gameID)})

        if gameFromDB is not None:

            TempGameplay= gameFromDB['gameplay']
            
            TempGrid = TempGameplay['grid']
            
            TempWinner= TempGameplay['winner']

            resp.media = {"status": "OK", "grid":TempGrid, "winner":TempWinner }

        else:
            resp.media = {"status": "ERROR",
                          "message": "Wrong ID"}
