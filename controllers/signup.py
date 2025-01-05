from flask_restful import Resource, reqparse 
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from hashlib import sha256
from models.User import User
from classes.errors import ERROR

class SignUp(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('phone', required=True, type=str, Location='json')
            parser.add_argument('password', required=True, type=str, Location='json')
            parser.add_argument('role', required=True, type=str, choices=['user', 'admin'], location='json')
            args = parser.parse_args()

            hashed_password = sha256(args['password'].encode('utf-8')).hexdigest()

            with session (autoflush=False, bind=self._connection) as db:
                new_user = User(
                    phone=args['phone'],
                    password = hashed_password,
                    role = args['role']
                )
                db.add(new_user)
                db.commit()

                return {"status": "OK", "message": "User registered successfully"}, 201
        except IntegrityError:
            return {"status": "ERROR", "message": "User already exist"}, 400
        except SQLAlchemyError as err:
            return {"status": "ERROR", "message": str(err)}, 500