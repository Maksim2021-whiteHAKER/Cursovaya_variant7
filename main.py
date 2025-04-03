from flask import Flask
from flask_restful import Api
from routers import InitRoutes
from flask_bcrypt import Bcrypt
from scheduler import start_scheduler

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
app.bcrypt = bcrypt

InitRoutes(api, app)

# Запуск планировщика
start_scheduler()

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)