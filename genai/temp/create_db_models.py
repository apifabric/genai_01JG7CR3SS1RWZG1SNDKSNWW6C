# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Player(Base):
    """description: Represents a player in the Settlers of Catan game."""
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    color = Column(String)

class Resource(Base):
    """description: Represents the resource types in the game (e.g. Brick, Wood)."""
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class PlayerResource(Base):
    """description: Junction table associating players with resources they own."""
    __tablename__ = 'player_resource'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    resource_id = Column(Integer, ForeignKey('resource.id'))
    amount = Column(Integer)

class City(Base):
    """description: Represents a city built by a player."""
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    location = Column(String)

class Settlement(Base):
    """description: Represents a settlement built by a player."""
    __tablename__ = 'settlement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    location = Column(String)

class Road(Base):
    """description: Represents a road built by a player."""
    __tablename__ = 'road'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    start_location = Column(String)
    end_location = Column(String)

class Trade(Base):
    """description: Represents trades between players."""
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_player_id = Column(Integer, ForeignKey('player.id'))
    to_player_id = Column(Integer, ForeignKey('player.id'))
    resource_id = Column(Integer, ForeignKey('resource.id'))
    amount = Column(Integer)

class DevelopmentCard(Base):
    """description: Represents development cards held by a player."""
    __tablename__ = 'development_card'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    type = Column(String)

class Tile(Base):
    """description: Represents a tile on the board and its resource type."""
    __tablename__ = 'tile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(Integer, ForeignKey('resource.id'))
    number = Column(Integer)

class DiceRoll(Base):
    """description: Represents the result of a dice roll."""
    __tablename__ = 'dice_roll'
    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(Integer)
    date_time = Column(DateTime)

class Game(Base):
    """description: Represents a single game instance."""
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime)

class GamePlayer(Base):
    """description: Junction table associating games with players."""
    __tablename__ = 'game_player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player_id = Column(Integer, ForeignKey('player.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    player1 = Player(id=1, name="Alice", color="Red")
    player2 = Player(id=2, name="Bob", color="Blue")
    resource1 = Resource(id=1, name="Brick")
    resource2 = Resource(id=2, name="Wood")
    player_resource1 = PlayerResource(id=1, player_id=1, resource_id=1, amount=5)
    player_resource2 = PlayerResource(id=2, player_id=1, resource_id=2, amount=3)
    city1 = City(id=1, player_id=1, location="A1")
    settlement1 = Settlement(id=1, player_id=1, location="B1")
    road1 = Road(id=1, player_id=1, start_location="A2", end_location="B2")
    
    
    
    session.add_all([player1, player2, resource1, resource2, player_resource1, player_resource2, city1, settlement1, road1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
