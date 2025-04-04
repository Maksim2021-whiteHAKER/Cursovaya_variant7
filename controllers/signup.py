from flask_restful import Resource, reqparse 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.user import User
from models.role import Role


class SignUp(Resource):
    def __init__(self, **kwargs):
        if 'connection' in kwargs:
            self._connection = kwargs['connection']
        if 'bcrypt' in kwargs:
            self._bcrypt = kwargs['bcrypt']

    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('firstname', required=True, type=str, location='json')
            parser.add_argument('middlename', required=False, type=str, location='json')
            parser.add_argument('surname', required=False, type=str, location='json')
            parser.add_argument('phone', required=True, type=str, location='json')
            parser.add_argument('email', required=False, type=str, location='json')
            parser.add_argument('password', required=True, type=str, location='json')
            parser.add_argument('role', required=True, type=str, choices=['user', 'admin'], location='json')
            args = parser.parse_args()

            hashed_password = self._bcrypt.generate_password_hash(args['password'])

            with Session (bind=self._connection) as db:

                # проверка на существование пользователя с таким же телефоном
                existing_user = db.query(User).filter(User.phone == args['phone']).first()
                if existing_user:
                    return {
                        "status": "ERROR",
                        "message": "User with this phone alredy exist",
                        "user_id": existing_user.id,
                    }, 409 # 409 conflict
                
                
                # получение роли
                role = db.query(Role).filter(Role.role_name == args['role']).first()
                if not role: return {"status", "ERROR", "message", "Role not found"}, 400

                new_user = User(
                    firstname = args['firstname'], # Имя
                    surname = args.get('surname'), # Фамилия
                    middlename = args.get('middlename'), # Отчество
                    phone = args['phone'],
                    email = args.get('email'),
                    password = hashed_password,
                    user_role = role.role_id
                )
                db.add(new_user)
                db.commit()

                return {"status": "OK", "message": "User registered successfully"}, 201
        except IntegrityError as err:
            return {
                "status": "ERROR",
                "message": "Database interity error",
                "code": "Duplicate entry",
                "details": str(err)
                }, 400
        except SQLAlchemyError as err:
            return {"status": "ERROR", "message": str(err)}, 500