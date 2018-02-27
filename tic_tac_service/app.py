import falcon
import routes
import middlewares


api_middle_wares = []

'''
#Used to test on local machine and some avoid CORS issues
from falcon_cors import CORS
cors_allow_all = CORS(allow_all_origins=True,
                      allow_all_headers=True,
                      allow_all_methods=True)
api_middle_wares.append(cors_allow_all.middleware)
'''

api_middle_wares.append(middlewares.Middleware())

api = falcon.API(
    middleware=api_middle_wares)
api.resp_options.secure_cookies_by_default = False
api = routes.addRoutes(api)
