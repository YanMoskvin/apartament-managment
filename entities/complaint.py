from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
class Complaint(base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    image_id = Column(String)
    resident_id = Column(String)
    status = Column(String)