
import falcon

class addUser:
    def on_post(self, req, resp):
        user = req.media
        user['enabled'] = False

        print(user)
        resp.media = user




