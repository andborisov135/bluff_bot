# self.game_id = game_id
# self.job_queue = job_queue
# self.job = None
# self.turn_duration = turn_duration  # in sec
# self.turn_start = None
# self.turn = 1
# self.whose_turn = created_player
# self.player_one = created_player
# self.player_two = None
# self.awaiting_player = self.player_two


from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine("postgresql+psycopg2://new_username:911610@/bluffdb")
Base = declarative_base(bind=engine)

class GameDB(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    player_one = Column(Integer)
    player_two = Column(Integer)
    turn_start = Column(Integer)#current turn start time

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.is_in_game = False
        self.balance = 0