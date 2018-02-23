import falcon
import routes
import middlewares


api = falcon.API(middleware=[middlewares.Middleware()])
api = routes.addRoutes(api)
    
