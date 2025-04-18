from flask_restful import Resource, reqparse 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.User import User


class SignUp(Resource):
    def __init__(self, **kwargs):
        if 'connection' in kwargs:
            self._connection = kwargs['connection']
        if 'bcrypt' in kwargs:
            self._bcrypt = kwargs['bcrypt']

    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('phone', required=True, type=str, location='json')
            parser.add_argument('password', required=True, type=str, location='json')
            parser.add_argument('role', required=True, type=str, choices=['user', 'admin'], location='json')
            args = parser.parse_args()

            hashed_password = self._bcrypt.generate_password_hash(args['password']).encode('utf-8')

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