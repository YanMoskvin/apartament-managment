from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB
from entities.complaint import Complaint
from entities.user import User
from entities.advert import Advert

db = create_engine(DB)
Session = sessionmaker(db)


def new_complaint():
    session = Session()
    new_complaint = Complaint(description="test", resident_id="1", status="new")
    session.add(new_complaint)
    session.commit()
    session.close()


def get_complaints():
    session = Session()
    complaints = session.query(Complaint)
    session.close()
    return complaints


def get_user(vk_id):
    session = Session()
    user = session.query(User).filter_by(vk_id=str(vk_id)).first()
    session.close()
    return user

def get_adverts():
    session = Session()
    adverts = session.query(Advert)
    session.close()
    return adverts