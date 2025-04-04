from flask_restful import reqparse
from classes.errors import ERROR
from controllers.controller_unauth import ControllerUnauth
from sqlalchemy.orm import Session
from flask import session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
import secrets
from datetime import datetime, timedelta
from models.user import User

class SignIn(ControllerUnauth):
    def __init__(self, **kwargs):
        if 'connection' in kwargs:
            self._connection = kwargs['connection']
        if 'bcrypt' in kwargs:
            self._bcrypt = kwargs['bcrypt']

    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('phone', required=True, type=str,location='json') 
            parser.add_argument('password', required=True, type=str,location='json')
            args = parser.parse_args()

            with Session(autoflush=False, bind=self._connection) as db:
                #создаем объект Person для добавления в бд
                user = db.query(User).filter(User.phone == args['phone']).one()

                if not self._bcrypt.check_password_hash(user.password, args['password']):
                    return self.make_response_str(ERROR.UNAUTHORIZED), 401
                
                # token(ключ) доступа
                access_token = secrets.token_hex(32)
                # refresh - обнова
                refresh_token = secrets.token_hex(32)

                user.hash_token = refresh_token
                user.token_created = datetime.now()

                # добавляем сессионую аутентификацию
                session['user_id'] = user.id
                session['access_token'] = access_token
                db.commit()

                data = {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'access_token_expiration': (datetime.now() + timedelta(minutes=30)).isoformat(),
                }
                return self.make_response_str(ERROR.OK, data), 200                
            
        except NoResultFound as e:
            return self.make_response_str(ERROR.OBJ_NOT_FOUND), 401
        except MultipleResultsFound as e:
           return self.make_response_str(ERROR.INTERNAL_ERROR), 500
        except (SQLAlchemyError, Exception) as e:
            response, code  = self.handle_exceptions(e)
            return response, code