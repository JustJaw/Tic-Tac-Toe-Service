import falcon
import routes
import middlewares


api = falcon.API(middleware=[middlewares.Middleware()])
api.resp_options.secure_cookies_by_default = False
api = routes.addRoutes(api)
    
