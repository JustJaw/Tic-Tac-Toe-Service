# game.py

import falcon

CLIENT_PLAYER = 'X'
SERVER_PLAYER = 'O'
EMPTY_SPACE = ' '
NO_WINNER_YET = ' '
TIE_WINNER = ' '
GRID_SIZE = 9
VECTOR_SIZE = 3


def get_win_vector(grid, player):
    if(grid.count(player) == VECTOR_SIZE):
        return player
    else:
        return NO_WINNER_YET


def determine_winner(grid, player):

    #Check Rows
    for i in range(0, VECTOR_SIZE):
        li = grid[i * VECTOR_SIZE: (i * VECTOR_SIZE) + VECTOR_SIZE]
        if(player == get_win_vector(li, player)):
            return player

    #Check Columns
    for i in range(0, VECTOR_SIZE):
        li = grid[i::VECTOR_SIZE]
        if(player == get_win_vector(li, player)):
            return player

    #Check Diagonals
    li1 = grid[0::VECTOR_SIZE + 1]
    li2 = list(grid[VECTOR_SIZE - 1:: VECTOR_SIZE - 1])[:-1]
    if(player == get_win_vector(li1, player)
       or player == get_win_vector(li2, player)):
        return player

    return NO_WINNER_YET


class PlayResource:
    def on_post(self, req, resp):
        try:
            grid = req.media['grid']
            winner = determine_winner(grid, CLIENT_PLAYER)
            if(winner != CLIENT_PLAYER):
                try:
                    i = grid.index(EMPTY_SPACE)
                    grid[i] = SERVER_PLAYER
                    winner = determine_winner(grid, SERVER_PLAYER)
                except ValueError:  # If there are no empty spaces left
                    winner = TIE_WINNER

            gameplay = {
                'grid': grid,
                'winner': winner
            }

            resp.media = gameplay

        except KeyError:
            print("\n======INVALID JSON=======\n" +
                  str(req.media) + "\n=========\n")
            raise falcon.HTTPBadRequest(
                'Invalid JSON'
            )


api = falcon.API()
api.add_route('/ttt/play', PlayResource())
