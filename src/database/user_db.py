from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine("postgresql+psycopg2://new_username:911610@/bluffdb")
Base = declarative_base(bind=engine)

class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.is_in_game = False
        self.balance = 0


# User.__table__.drop(engine)


Base.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()

user = UserDB(name="Andrew", id=1)

session.add(user)
session.commit()

print("----------")
print(session.query(User.id).filter_by(id=1).scalar())
print("============")

