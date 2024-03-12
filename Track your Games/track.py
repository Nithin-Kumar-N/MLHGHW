from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create engine and session
engine = create_engine('sqlite:///game_tracker.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define base class for declarative base
Base = declarative_base()

# Define Player model
class Player(Base):
    __tablename__ = 'players'
    player_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # Add other fields as needed
    games = relationship('Game', back_populates='player')
    characters = relationship('Character', back_populates='player')

# Define Game model
class Game(Base):
    __tablename__ = 'games'
    game_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False)
    game_name = Column(String, nullable=False)
    date_completed = Column(DateTime, default=datetime.now)
    # Add other fields as needed
    player = relationship('Player', back_populates='games')

# Define Character model
class Character(Base):
    __tablename__ = 'characters'
    character_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False)
    character_name = Column(String, nullable=False)
    # Add other fields as needed
    player = relationship('Player', back_populates='characters')

# Define HighScore model
class HighScore(Base):
    __tablename__ = 'high_scores'
    score_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.game_id'), nullable=False)
    score = Column(Integer, nullable=False)
    # Add other fields as needed

# Create tables in the database
Base.metadata.create_all(engine)
