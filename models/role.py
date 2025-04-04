from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app_data.db_config import Base

class Role(Base):
    __tablename__ = 'role'
    role_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    role_name = Column(String(20), nullable=False)
    users = relationship('User', back_populates='role')

    @property
    def serialize(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name
        }