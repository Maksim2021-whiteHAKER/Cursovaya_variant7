from controllers.sayhello import SayHello, SiteHello 
from controllers.server_version import ServerVersion 
from controllers.device_state import DeviceState
from controllers.signin import SignIn
from controllers.signup import SignUp
from controllers.device_state import Notification, SensorData, DeviceErrors
from app_data.db_config import my_connect
from controllers.token_refresh import TokenRefresh
from controllers.admin_logs import AdminLogs

def InitRoutes(api, app):

        additional_params = {
                'connection': my_connect,
                    'bcrypt': app.bcrypt # Доступ к bcrypt 
        }

        api.add_resource(SiteHello, '/')                                                             # V
        api.add_resource(SayHello, '/api/v1/hello')                                                  # V
        api.add_resource(ServerVersion, '/api/version')                                              # V
        api.add_resource(DeviceState, '/api/v1/state', resource_class_kwargs=additional_params)      # V
        api.add_resource(SignIn, '/api/v1/auth', resource_class_kwargs=additional_params)            # V
        api.add_resource(SignUp, '/api/v1/signup', resource_class_kwargs=additional_params)          # V
        api.add_resource(Notification, '/api/notification', resource_class_kwargs=additional_params) # V
        api.add_resource(SensorData, '/api/sensors', resource_class_kwargs=additional_params)        # V
        api.add_resource(DeviceErrors, '/api/errors', resource_class_kwargs=additional_params)       # V
        api.add_resource(TokenRefresh, '/api/v1/token', resource_class_kwargs=additional_params)     # V
        api.add_resource(AdminLogs, '/api/admin/logs', resource_class_kwargs=additional_params)      # V "logs": []