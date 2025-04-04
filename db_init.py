#from app_data.definitions import my_connect
from models.user import User
from models.state import AquaState
from app_data.db_config import Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

passwordForUser1 = "1569"
passwordForUser2 = "6841" # for phone 79651284649, 

hashPass = bcrypt.generate_password_hash(passwordForUser1).decode('utf-8')

connection_str = "mysql+pymysql://user:password+@localhost/aqua_db"
my_connect = create_engine(connection_str)
Base.metadata.create_all(bind=my_connect)

with Session(autoflush=False, bind=my_connect) as db:
    # создаем объект Person для добавления в бд
    user = User(
        surname = 'Ivanov',
        firstname = 'Ivan',
        middlename = 'Ivanovich',
        phone = '89121234567',
        email = 'ivanov@mail.ru',
        password = hashPass,
        hash_token =  None,
        token_created = None )
    db.add(user)     # добавляем в бд


    d1 = AquaState(
        name = 'Air pump',
        type = 'switch',
        status = 0,
    )
    d2 = AquaState(
        name = 'Light',
        type = 'switch',
        status = 0,
    )
    d3 = AquaState(
        name = 'Temperature sensor',
        type = 'temperature',
        status = 25,
    )
    
    db.add_all([d1, d2, d3])
    db.commit()     # сохраняем изменения
    print(user.id)   # можно получить установленный id