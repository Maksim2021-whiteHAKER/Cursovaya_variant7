from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app_data.definitions import Base


class NotificationSettings(Base):
    __tablename__ = 'notification_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    threshold = Column(Float)

    # добавление индекса для быстрого поиска
    __table_args__ = (
        Index('ix_notify_device_threshold', 'device_id', 'threshold'),
    )

    # связь
    device = relationship("AquaState", back_populates="notifications")
    user = relationship("User")