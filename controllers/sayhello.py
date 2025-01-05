from flask_restful import Resource

class SayHello(Resource):
    def get(self):
        return {'hello, im, version: ': 0}
