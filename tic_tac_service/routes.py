import falcon
import Controller.GameController as GameController
import Controller.UserController as UserController

def addRoutes(api):
    api.add_route('/ttt/play', game.PlayResource())
    api.add_route('/adduser', UserResource.addUser())
    api.add_route('/verify', UserResource.verifyUser())
    api.add_route('/getcookie', UserResource.cookieTest())
    api.add_route('/login', UserResource.login())
    api.add_route('/logout', UserResource.logout())
    api.add_route('/listgames', GameController.GamesResource())
    return api
