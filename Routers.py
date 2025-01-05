from controllers.sayhello import SayHello
from controllers.server_version import ServerVersion 
from controllers.device_state import DeviceState
from controllers.signin import SignIn
from app_data.definitions import my_connect

def InitRoutes(api):

        additional_params = {
                'connection': my_connect,
        }

        api.add_resource(SayHello, '/api/v1/hello')
        api.add_resource(ServerVersion, '/api/version')
        api.add_resource(DeviceState, '/api/v1/state')
        api.add_resource(SignIn, '/api/v1/auth', resource_class_kwargs=additional_params)