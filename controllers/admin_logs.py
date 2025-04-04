from flask_restful import Resource
from .controller_base import ControllerBase
from models.log_config import Log
from models.user import User  # Импорт модели User
from sqlalchemy.orm import Session
from classes.errors import ERROR
from sqlalchemy.exc import SQLAlchemyError

class AdminLogs(ControllerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Наследование ControllerBase
        self._connection = kwargs.get('connection')

    def get(self):
        try:
            with Session(autoflush=False, bind=self._connection) as db:
                # Проверка роли пользователя
                user = db.query(User).get(self.user_id)
                if not user or user.role.role_name != 'admin':
                    return self.make_response_str(
                        ERROR.UNAUTHORIZED,
                        message="Доступ только для администратора"
                    ), 403

                # Получение логов
                logs = db.query(Log).order_by(
                    Log.timestamp.desc()
                ).limit(100).all()
                
                logs_data = [{
                    'id': log.id,
                    'user_id': log.user_id,
                    'action': log.action,
                    'timestamp': log.timestamp.isoformat()
                } for log in logs]
                
                return self.make_response_str(
                    ERROR.OK,
                    data=logs_data
                ), 200

        except SQLAlchemyError as e:
            # Обработка ошибок БД через родительский метод
            response, code = self.handle_exceptions(e)
            return response, code