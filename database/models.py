# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 28, 2024 19:44:23
# Database: sqlite:////tmp/tmp.tieNfjVMJ2-01JG7CR3SS1RWZG1SNDKSNWW6C/CatanManagerDB/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class DiceRoll(SAFRSBaseX, Base):
    """
    description: Represents the result of a dice roll.
    """
    __tablename__ = 'dice_roll'
    _s_collection_name = 'DiceRoll'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    roll_number = Column(Integer)
    date_time = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)



class Game(SAFRSBaseX, Base):
    """
    description: Represents a single game instance.
    """
    __tablename__ = 'game'
    _s_collection_name = 'Game'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    GamePlayerList : Mapped[List["GamePlayer"]] = relationship(back_populates="game")



class Player(SAFRSBaseX, Base):
    """
    description: Represents a player in the Settlers of Catan game.
    """
    __tablename__ = 'player'
    _s_collection_name = 'Player'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CityList : Mapped[List["City"]] = relationship(back_populates="player")
    DevelopmentCardList : Mapped[List["DevelopmentCard"]] = relationship(back_populates="player")
    GamePlayerList : Mapped[List["GamePlayer"]] = relationship(back_populates="player")
    PlayerResourceList : Mapped[List["PlayerResource"]] = relationship(back_populates="player")
    RoadList : Mapped[List["Road"]] = relationship(back_populates="player")
    SettlementList : Mapped[List["Settlement"]] = relationship(back_populates="player")
    TradeList : Mapped[List["Trade"]] = relationship(foreign_keys='[Trade.from_player_id]', back_populates="from_player")
    toTradeList : Mapped[List["Trade"]] = relationship(foreign_keys='[Trade.to_player_id]', back_populates="to_player")



class Resource(SAFRSBaseX, Base):
    """
    description: Represents the resource types in the game (e.g. Brick, Wood).
    """
    __tablename__ = 'resource'
    _s_collection_name = 'Resource'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    PlayerResourceList : Mapped[List["PlayerResource"]] = relationship(back_populates="resource")
    TileList : Mapped[List["Tile"]] = relationship(back_populates="resource")
    TradeList : Mapped[List["Trade"]] = relationship(back_populates="resource")



class City(SAFRSBaseX, Base):
    """
    description: Represents a city built by a player.
    """
    __tablename__ = 'city'
    _s_collection_name = 'City'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey('player.id'))
    location = Column(String)

    # parent relationships (access parent)
    player : Mapped["Player"] = relationship(back_populates=("CityList"))

    # child relationships (access children)



class DevelopmentCard(SAFRSBaseX, Base):
    """
    description: Represents development cards held by a player.
    """
    __tablename__ = 'development_card'
    _s_collection_name = 'DevelopmentCard'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey('player.id'))
    type = Column(String)

    # parent relationships (access parent)
    player : Mapped["Player"] = relationship(back_populates=("DevelopmentCardList"))

    # child relationships (access children)



class GamePlayer(SAFRSBaseX, Base):
    """
    description: Junction table associating games with players.
    """
    __tablename__ = 'game_player'
    _s_collection_name = 'GamePlayer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    game_id = Column(ForeignKey('game.id'))
    player_id = Column(ForeignKey('player.id'))

    # parent relationships (access parent)
    game : Mapped["Game"] = relationship(back_populates=("GamePlayerList"))
    player : Mapped["Player"] = relationship(back_populates=("GamePlayerList"))

    # child relationships (access children)



class PlayerResource(SAFRSBaseX, Base):
    """
    description: Junction table associating players with resources they own.
    """
    __tablename__ = 'player_resource'
    _s_collection_name = 'PlayerResource'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey('player.id'))
    resource_id = Column(ForeignKey('resource.id'))
    amount = Column(Integer)

    # parent relationships (access parent)
    player : Mapped["Player"] = relationship(back_populates=("PlayerResourceList"))
    resource : Mapped["Resource"] = relationship(back_populates=("PlayerResourceList"))

    # child relationships (access children)



class Road(SAFRSBaseX, Base):
    """
    description: Represents a road built by a player.
    """
    __tablename__ = 'road'
    _s_collection_name = 'Road'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey('player.id'))
    start_location = Column(String)
    end_location = Column(String)

    # parent relationships (access parent)
    player : Mapped["Player"] = relationship(back_populates=("RoadList"))

    # child relationships (access children)



class Settlement(SAFRSBaseX, Base):
    """
    description: Represents a settlement built by a player.
    """
    __tablename__ = 'settlement'
    _s_collection_name = 'Settlement'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey('player.id'))
    location = Column(String)

    # parent relationships (access parent)
    player : Mapped["Player"] = relationship(back_populates=("SettlementList"))

    # child relationships (access children)



class Tile(SAFRSBaseX, Base):
    """
    description: Represents a tile on the board and its resource type.
    """
    __tablename__ = 'tile'
    _s_collection_name = 'Tile'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    resource_id = Column(ForeignKey('resource.id'))
    number = Column(Integer)

    # parent relationships (access parent)
    resource : Mapped["Resource"] = relationship(back_populates=("TileList"))

    # child relationships (access children)



class Trade(SAFRSBaseX, Base):
    """
    description: Represents trades between players.
    """
    __tablename__ = 'trade'
    _s_collection_name = 'Trade'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    from_player_id = Column(ForeignKey('player.id'))
    to_player_id = Column(ForeignKey('player.id'))
    resource_id = Column(ForeignKey('resource.id'))
    amount = Column(Integer)

    # parent relationships (access parent)
    from_player : Mapped["Player"] = relationship(foreign_keys='[Trade.from_player_id]', back_populates=("TradeList"))
    resource : Mapped["Resource"] = relationship(back_populates=("TradeList"))
    to_player : Mapped["Player"] = relationship(foreign_keys='[Trade.to_player_id]', back_populates=("toTradeList"))

    # child relationships (access children)
