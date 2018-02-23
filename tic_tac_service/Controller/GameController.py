# Module: GameController.py

import falcon
import dbmongo as DB
from pymongo import MongoClient
from bson import json_util, ObjectId

CLIENT_PLAYER = 'X'
SERVER_PLAYER = 'O'
EMPTY_SPACE = ' '
NO_WINNER_YET = ' '
TIE_WINNER = ' '
GRID_SIZE = 9
VECTOR_SIZE = 3
EMPTY_GRID = [EMPTY_SPACE] * GRID_SIZE

last_move_index = 0



def get_win_vector(grid, player):
    if(grid.count(player) == VECTOR_SIZE):
        return player
    else:
        return NO_WINNER_YET

def determine_winner(grid,player):

    #Check Rows
    for i in range(0, VECTOR_SIZE):
        li = grid[i*VECTOR_SIZE: (i*VECTOR_SIZE) + VECTOR_SIZE]
        if(player == get_win_vector(li,player)):
            return player

    #Check Columns
    for i in range(0, VECTOR_SIZE):
        li = grid[i::VECTOR_SIZE]
        if(player == get_win_vector(li, player)):
            return player

    #Check Diagonals
    li1 = grid[0::VECTOR_SIZE+1]
    li2 = list(grid[VECTOR_SIZE - 1 :: VECTOR_SIZE - 1])[:-1]
    if(player == get_win_vector(li1, player) 
    or player == get_win_vector(li2, player)):
        return player
    
    return NO_WINNER_YET


def save_complete_game(gameplay,user_id,user):
    if gameplay.winner is CLIENT_PLAYER:
        winnerName = "human"
    elif gameplay.winner is SERVER_PLAYER:
        winnerName = "wopr"
    elif gameplay.winner is TIE_WINNER:
        winnerName = "tie"
    
    

    userFromDB = usersCollection.find_one_and_update({'_id': userFromDB['_id']}, {
        "$inc": user_enabled}, return_document=ReturnDocument.AFTER)

    game = {
        "user_id": user_id,
        "id" : " ", #id for the game that is automatically set in mongo,
        "gameplay" : gameplay
        "start_date": " ", #start date for the game 
    }

    DB.games.insert

    #DB.users




class PlayResource:

    no_auth = True

    def on_post(self, req, resp):
        try:
            grid = req.media['grid']
            move = req.media['move']
            winner = NO_WINNER_YET

            user_id = req.cookies['theCookie']

            usersCollection.find_one({"_id": user_id})
            
            if move is not None:
                winner = determine_winner(grid, CLIENT_PLAYER)
                if(winner != CLIENT_PLAYER): 
                    try:
                        move = grid.index(EMPTY_SPACE)
                        grid[move] = SERVER_PLAYER
                        winner = determine_winner(grid, SERVER_PLAYER)
                    except ValueError: # If there are no empty spaces left
                        winner = TIE_WINNER

            gameplay = {
                'grid': grid,
                'winner': winner,
                'move': move
            }


            # Clear grid and saves game if winner is decided
            if (winner is CLIENT_PLAYER or winner is SERVER_PLAYER or winner is TIE_WINNER):
                #save_complete_game(gameplay, user_id)
                grid = EMPTY_GRID

            

            resp.media = gameplay

        except KeyError:
            print("\n======INVALID JSON=======\n" + str(req.media) + "\n=========\n")
            raise falcon.HTTPBadRequest(
                'Invalid JSON'
            )

class GamesResource:
    no_auth = True

    def on_get(self, req, resp):
        games = DB.games.find()
        
        resp.body = json_util.dumps(games)


########### added by teddy onwards
class listgames:

    no_auth = True

    def on_post(self, req, resp):

        games = DB.games.find()
        
        resp.body = json_util.dumps(games)
        return;


class getgame:

    no_auth = True

    def on_post(self, req, resp):

        Tempgame=req.media

        gameID= Tempgame['id'] 
        
        gameFromDB = games.find_one({"id": gameID})

        if gameFromDB is not None:

            TempGameplay= gameFromDB['gameplay']
            
            TempGrid = TempGameplay['grid']
            
            TempWinner= TempGameplay['winner']

            resp.media = {"Status": "Ok", "grid":TempGrid, "winner":TempWinner }

        else:
            resp.body="Wrong ID"
