# sample.py

import falcon

class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote
        #resp.status = falcon.HTTP_200 #By default 200 ok is returned
        print(req)

class TestResource:
    #@falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):

        print(req.media)
        try:
            doc = req.media['doc']

            gson = {
                'g': [
                    {"quote": "WOAH"},
                    {"quote": "WOW!"}
                ],
                'doc': doc
            }
            resp.media = gson
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body. "doc" is missing')
    

api = falcon.API()
api.add_route('/ttt/play/quote', QuoteResource())
api.add_route('/ttt/play', TestResource())
