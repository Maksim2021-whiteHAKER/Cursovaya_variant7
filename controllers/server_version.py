from flask_restful import Resource

class ServerVersion(Resource):
    def get(self):
        return {
            'error': 0,
            'message': "OK",
            'data': {
                'SERVER version': '0.0.1'
            }
        }, 200
    