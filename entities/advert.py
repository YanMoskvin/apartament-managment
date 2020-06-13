from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
class Advert(base):
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True)
    text = Column(String)