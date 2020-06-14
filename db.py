from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB
from entities.advert import Advert
from entities.complaint import Complaint
from entities.user import User

db = create_engine(DB)
Session = sessionmaker(db)


def add_advert(text, option_1=None, option_2=None, option_3=None):
    session = Session()
    new_advert = Advert(text=text, option_1=option_1, option_2=option_2, option_3=option_3, voice_1='0', voice_2='0',
                        voice_3='0')
    session.add(new_advert)
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


def get_adverts_by_id(id):
    session = Session()
    advert = session.query(Advert).filter_by(id=id).first()
    session.close()
    return advert


def update_advert(id, voice_1=None, voice_2=None, voice_3=None):
    session = Session()
    advert = session.query(Advert).filter_by(id=id).first()
    if voice_1 != None:
        advert.voice_1 = str(int(advert.voice_1) + int(voice_1))
    if voice_2 != None:
        advert.voice_2 = str(int(advert.voice_2) + int(voice_2))
    if voice_3 != None:
        advert.voice_3 = str(int(advert.voice_3) + int(voice_3))
    session.commit()
