import falcon
import Controller.GameController as GameController
import Controller.UserController as UserController

def addRoutes(api):
    api.add_route('/ttt/play', GameController.PlayResource())
    api.add_route('/listgames', GameController.GamesResource())
    api.add_route('/adduser', UserController.addUser())
    api.add_route('/verify', UserController.verifyUser())
    api.add_route('/getcookie', UserController.cookieTest())
    return api
