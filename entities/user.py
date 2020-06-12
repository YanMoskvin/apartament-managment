from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    vk_id = Column(String)