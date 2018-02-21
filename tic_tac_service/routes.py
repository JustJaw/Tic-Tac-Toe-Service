import falcon
import game
import Controller.UserController as UserResource

def addRoutes(api):
    api.add_route('/ttt/play', game.PlayResource())
    api.add_route('/adduser', UserResource.addUser())
    return api
