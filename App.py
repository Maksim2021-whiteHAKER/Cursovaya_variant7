from flask import Flask
from flask_restful import Api
from Routers import InitRoutes
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api(app)

# Инициализация bcrypt
bcrypt = Bcrypt(app)
# Прикрепление к приложению, для доступа из других модулей
app.bcrypt = bcrypt

InitRoutes(api, app)
        
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

# ExecStart=
# ExecStart=/usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid --skip-grant-tables --skip-networking
