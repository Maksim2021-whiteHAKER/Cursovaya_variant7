from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app_data.definitions import Base


class NotificationSettings(Base):
    __tablename__ = 'notification_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey=('user.id'))
    device_id = Column(Integer, ForeignKey=('device.id'))
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    critical_value = Column(float, nullable=True)