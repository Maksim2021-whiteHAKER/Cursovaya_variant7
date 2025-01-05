from models.User import User
from models.State import AquaState
#from app_data.definitions import my_connect
from app_data.definitions import Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


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
        password = '123',
        hash_token =  None,
        token_created = None )
    db.add(user)     # добавляем в бд


    d1 = AquaState(
        device_name = 'Air pump',
        device_type = 'switch',
        device_status = 0,
    )
    d2 = AquaState(
        device_name = 'Light',
        device_type = 'switch',
        device_status = 0,
    )
    d3 = AquaState(
        device_name = 'Temperature sensor',
        device_type = 'sensor',
        device_status = 25,
    )
    db.add_all([d1, d2, d3])
    db.commit()     # сохраняем изменения
    print(user.id)   # можно получить установленный id