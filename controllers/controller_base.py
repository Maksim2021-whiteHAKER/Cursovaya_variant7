from flask_restful import reqparse, abort
from classes.errors import APIError, ERROR
from controllers.controller_unauth import ControllerUnauth
from sqlalchemy.orm import Session
from models.user import User
from flask import session
from datetime import datetime, timedelta

class ControllerBase(ControllerUnauth):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('authorization', required=False, type=str,location='headers', help = 'Missing authorization token')    

    def __init__(self, *args, **kwargs):
        try:
            # если Bearer token отсутствует или не совпадает то выдаем 401
            super().__init__(**kwargs)
            args = ControllerBase.parser.parse_args()
            self.abort_if_authorization_error(args['authorization'])

        except Exception as e:
            abort(401, error = 1, message=APIError.err(ERROR.UNAUTHORIZED),data=None)    

    # проверка авторизованности
    def abort_if_authorization_error(self, auth: str):
        if not auth:
            abort(401, error = 1, message=APIError.err(ERROR.UNAUTHORIZED), data=None)
        items = auth.split(' ')
        if len(items) < 2:
            abort(401, error = 1, message=APIError.err(ERROR.UNAUTHORIZED), data=None)
        user_token = items[1]
        if not self.is_valid_token(user_token): 
            abort(401, error = 1, message=APIError.err(ERROR.UNAUTHORIZED), data=None)

    #проверка токена
       # Проверка токена в БД пользователей
    def is_valid_token(self, token):
        if 'access_token' in session and session['access_token'] == token:
            self.user_id = session['user_id']
            return True
        with Session(autoflush=False, bind=self._connection) as db:
            user = db.query(User).filter(
                User.hash_token == token,
                User.token_created >= datetime.now() - timedelta(minutes=30)
            ).first()
            if user:
                self.user_id = user.id 
                return True
        return False    
