import falcon
import game
import Controller.UserController as UserResource

def addRoutes(api):
    api.add_route('/ttt/play', game.PlayResource())
    api.add_route('/adduser', UserResource.addUser())
    api.add_route('/verify', UserResource.verifyUser())
    api.add_route('/getcookie', UserResource.cookieTest())
    api.add_route('/login', UserResource.cookieTest())
    api.add_route('/logout', UserResource.cookieTest())
    return api
