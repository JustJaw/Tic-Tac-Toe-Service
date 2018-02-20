import falcon
import game

api = falcon.API()
api.add_route('/ttt/play', game.PlayResource())
#api.add_route('/adduser')
