from flask_restful import Resource

class SayHello(Resource):
    def get(self):
        return {'hello, im, version: ': 0}
    
class SiteHello(Resource):
    def get(self):
        return {'hello, im a site for for online reading from a portable weather station': 0}
