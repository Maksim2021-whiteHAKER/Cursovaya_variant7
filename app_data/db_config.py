from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass
mysql_user = 'user'
mysql_passw = 'password+'
mysql_achemy_connect_str = f"mysql+pymysql://{mysql_user}:{mysql_passw}@localhost/aqua_db"

my_connect = create_engine(mysql_achemy_connect_str)