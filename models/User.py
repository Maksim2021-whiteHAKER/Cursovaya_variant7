from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app_data.definitions import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False) #key
    surname = Column(String(30), nullable=True)
    firstname = Column(String(30), nullable=False)
    middlename = Column(String(30), nullable=True)
    phone = Column(String(12), nullable=False)
    email = Column(String(60), nullable=True)
    password = Column(String(128), nullable=False)
    hash_token = Column(String(128), nullable=True)
    token_created = Column(DateTime(), nullable=True)
    user_role = Column(Integer, ForeignKey('role.role_id'), nullable=True)
    role = relationship('Role', back_populates='users')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'firstname': self.firstname,
            'middlename': self.middlename,
            'phone': self.phone,
            'password': self.password,
            'hash_token': self.hash_token,
            'token_created': self.token_created,
            'user_role': self.user_role,
            'role': self.role            
        }