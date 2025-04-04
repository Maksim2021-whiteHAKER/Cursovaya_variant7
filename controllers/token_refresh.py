from flask_restful import reqparse
from classes.errors import ERROR
from controllers.controller_unauth import ControllerUnauth
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
import secrets
from datetime import datetime, timedelta
from models.user import User
from hashlib import sha256

class TokenRefresh(ControllerUnauth):
    def __init__(self, **kwargs):
        if 'connection' in kwargs:
            self._connection = kwargs['connection']
        if 'bcrypt' in kwargs:
            self._bcrypt = kwargs['bcrypt']

    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('refresh_token', required=True, type=str,location='json') 
            args = parser.parse_args()

            with Session(autoflush=False, bind=self._connection) as db:
                # Поиск пользователя по обновленному ключу(token)
                refresh_token_hash = sha256(args['refresh_token'].encode('utf-8')).hexdigest()
                user = db.query(User).filter(User.hash_token == refresh_token_hash).one()

                if not user:
                    return self.make_response_str(ERROR.UNAUTHORIZED), 401
                
                # token(ключ) доступа
                access_token = secrets.token_hex(32)
                # refresh - обнова
                new_refresh_token = secrets.token_hex(32)

                user.hash_token = sha256(new_refresh_token.encode('utf-8')).hexdigest()
                user.token_created = datetime.now()
                db.commit()

                data = {
                    'access_token': access_token,
                    'refresh_token': new_refresh_token,
                    'access_token_expiration': (datetime.now() + timedelta(minutes=30)).isoformat(),
                }
                return self.make_response_str(ERROR.OK, data), 200                
            
        except NoResultFound as e:
            return self.make_response_str(ERROR.UNAUTHORIZED), 401
        except MultipleResultsFound as e:
           return self.make_response_str(ERROR.INTERNAL_ERROR), 500
        except (SQLAlchemyError, Exception) as e:
            response, code  = self.handle_exceptions(e)
            return response, code