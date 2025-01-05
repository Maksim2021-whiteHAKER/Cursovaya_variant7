from sqlalchemy import Column, Integer, String, SmallInteger
from app_data.definitions import Base

class AquaState(Base):
    __tablename__ = "state"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False) #key
    device_name = Column(String(30))
    device_type = Column(String(30))
    device_status = Column(SmallInteger)

    # сериализатор
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.device_name,
            'type': self.device_status,
        }