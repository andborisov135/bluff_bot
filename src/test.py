# import logging
#
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:', echo=True)
#
# from sqlalchemy import Column, Integer, String, Sequence
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
#     name = Column(String(50))
#     fullname = Column(String(50))
#     password = Column(String(12))
#
#     def __repr__(self):
#         return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
#
#
# print(User.__table__ )


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "person"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, unique=True)


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()
user = User()
user.id = 0
user.username = "alice"

session.add(user)
session.commit()
session.close()

users = session.query(User).all()
print(1111111111111111111111)

exists = session.query(User.id).filter_by(username='alice').scalar() is not None
print(exists)
print(11111111111)

# for user in users:
#     print("User with username=%s and id=%d" % (user.username, user.id,))

session.close()
