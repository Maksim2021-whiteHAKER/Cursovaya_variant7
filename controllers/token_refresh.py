from flask_restful import reqparse
from classes.errors import ERROR
from controllers.controller_base import ControllerBase
from sqlalchemy.orm import Session
from flask import session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
import secrets
from datetime import datetime, timedelta
from models.user import User

class TokenRefresh(ControllerBase):  # Наследуем от ControllerBase
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Инициализация ControllerBase
        if 'bcrypt' in kwargs:
            self._bcrypt = kwargs['bcrypt']

    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('refresh_token', required=True, type=str, location='json')
            args = parser.parse_args()

            with Session(autoflush=False, bind=self._connection) as db:
                # Ищем пользователя по refresh_token (как в DeviceState)
                user = db.query(User).filter(
                    User.hash_token == args['refresh_token'],  # Прямое сравнение
                    User.token_created >= datetime.now() - timedelta(days=7)
                ).first()

                if not user:
                    return self.make_response_str(ERROR.UNAUTHORIZED), 401

                # Генерируем новые токены
                new_access_token = secrets.token_hex(32)
                new_refresh_token = secrets.token_hex(32)

                # Обновляем токены в БД
                user.hash_token = new_refresh_token
                user.token_created = datetime.now()
                db.commit()

                # Обновляем сессию (как в ControllerBase)
                session['access_token'] = new_access_token
                session['user_id'] = user.id

                return self.make_response_str(ERROR.OK, {
                    'access_token': new_access_token,
                    'refresh_token': new_refresh_token,
                    'expires_in': 1800  # 30 минут
                }), 200

        except SQLAlchemyError as e:
            return self.handle_exceptions(e)