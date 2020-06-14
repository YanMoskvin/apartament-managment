from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Advert(base):
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    option_1 = Column(String)
    option_2 = Column(String)
    option_3 = Column(String)
    voice_1 = Column(String)
    voice_2 = Column(String)
    voice_3 = Column(String)
