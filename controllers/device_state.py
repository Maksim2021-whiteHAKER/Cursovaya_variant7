from flask_restful import Resource, reqparse
from controllers.controller_base import ControllerBase
from app_data.devices_manager import get_device_data, set_device_data
from classes.errors import APIError, ERROR
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
from models.state import AquaState
from models.notification_settings import NotificationSettings
from services.action_logger import log_action

class DeviceState(ControllerBase):
    def get(self):
        try:
            parser = DeviceState.parser.copy()
            parser.add_argument('deviceId', type=int, location='args', required=True)
            args = parser.parse_args()  

            with Session(autoflush=False, bind=self._connection) as db:
                #оздаем объект Person для добавления в бд
                device = db.query(AquaState)\
                    .filter(
                        AquaState.id == args['deviceId']
                    ).first()
            if device != None:
                return self.make_response_str(ERROR.OK, device.serialize), 200
            return self.make_response_str(ERROR.UNKNOWN_DEVICE), 200
        except (SQLAlchemyError, Exception) as e:
            response, code  = self.handle_exceptions(e)
            return response, code
            
            
    def post(self):
        try:
             parser = DeviceState.parser.copy()
             parser.add_argument('deviceId', type=int, location='json', required=True)    
             parser.add_argument('value', type=int, location='json', required=True)  
             args = parser.parse_args()

             with Session(autoflush=False, bind=self._connection) as db:  #Cоздаем объект Person для добавления в бд
                   device = db.query(AquaState)\
                .filter(AquaState.id == args['deviceId']).first()
                   
                   if device == None:
                    return self.make_response_str(ERROR.UNKNOWN_DEVICE), 200 
                   
                   if device.device_type == 'sensor':
                    return self.make_response_str(ERROR.UNABLE_CHANGE), 200      
                   
                   device.device_status = args['value']
                   db.commit()

                   # Логгирование действия
                   log_action(self._connection, user_id=self.user_id, action=f"Changed device {device.id} status")
                   
                   return self.make_response_str(ERROR.OK, device.serialize), 200
             
        except (SQLAlchemyError, Exception) as e:
            response, code  = self.handle_exceptions(e)
            return response, code
        
    def get_device(self, user_role, user_id):
        try:
            with Session(autoflush=False, bind=self._connection) as db:
                if user_role == "admin":
                    devices = db.query(AquaState).all()
                else:
                    devices = db.query(AquaState).filter(AquaState.owner_id == user_id).all()
                
                return [device.serialize for device in devices], 200
        except SQLAlchemyError as err:
            responce, code = self.handle_exceptions(err)
            return responce, code
        
class SensorData(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('deviceId', type=int, required=True, location='args')
            args = parser.parse_args()

            with Session(autoflush=False, bind=self._connection) as db:
                device = db.query(AquaState).filter(AquaState.id == args['deviceId']).first()

                if device is None:
                    return {"status": "ERROR", "message": "device not found"}, 404
                
                if device.device_type != 'sensor':
                    return {"status": "ERROR", "message": "Not a sensor device"}, 400
                
                return {"status": "OK", "data": device.readings}, 200
        except SQLAlchemyError as err:
            return {"status": "ERROR", "message": str(err)}, 500

class Notification(ControllerBase):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('device_id', type=int, required=False, location='json')
            parser.add_argument('email', type=str, required=False, location='json')
            parser.add_argument('phone', type=str, required=False, location='json')
            parser.add_argument('threshold', type=float, required=False, location='json')
            args = parser.parse_args()

            with Session(autoflush=False, bind=self._connection) as db:
                new_setting = NotificationSettings(
                    user_id = self.user_id, # Получить из токена(это ключ)
                    device_id = args['device_id'],
                    email = args.get('email'),
                    phone = args.get('phone'),                    
                    threshold = args.get('threshold')
                )
                db.add(new_setting)
                db.commit()

                return {"status": "OK", "message": 'Notification settings updated'}, 201
        except SQLAlchemyError as e:
            return {"status": "ERROR", "message": str(e)}, 500

class DeviceErrors(Resource):
    def get(self):
        try:
            with Session(autoflush=False, bind=self._connection) as db:
                errors = db.query(AquaState).filter(AquaState.error_code.isnot(None)).all()
                return [error.serialize for error in errors], 200
        except SQLAlchemyError as e:
             return {"status": "ERROR", "message": str(e)}, 500