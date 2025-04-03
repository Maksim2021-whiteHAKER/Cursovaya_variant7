from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from app_data.definitions import Base

class AquaState(Base):
    __tablename__ = "devices"  # Более точное имя таблицы
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(Enum('temperature', 'humidity', 'pressure', 'switch', name='device_types'))
    status = Column(SmallInteger)
    value = Column(Float)  # Для числовых показаний датчиков
    error_code = Column(String(20), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    # Связи
    notifications = relationship("NotificationSettings", back_populates="device")
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'value': self.value,
            'error': self.error_code
        }