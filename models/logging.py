from app_data.definitions import Base
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session
from datetime import datetime

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


def log_action(connection, user_id, action):
    with Session(autoflush=False, bind=connection) as db:
        log_entry = Log(user_id = user_id, action = action)
        db.add(log_entry)
        db.commit()
