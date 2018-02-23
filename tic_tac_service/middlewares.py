import falcon

class Middleware(object):

    #Process the request before routing it.
    #def process_request(self, req, resp):
    #    
    
    #Process the request after routing.
    def process_resource(self, req, resp, resource, params):
        if 'theCookie' not in req.cookies and not hasattr(resource, 'no_auth'):
            raise falcon.HTTPBadRequest(
               'Cookie',
               'No Cookie Provided')
        
            
    #Post-processing of the response (after routing).
    #def process_response(self, req, resp, resource, req_succeeded):
    

        
