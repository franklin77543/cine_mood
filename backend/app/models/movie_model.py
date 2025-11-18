from sqlalchemy import Column, String, Integer, Date, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid
from datetime import datetime


class Movie(Base):
    """電影主表 - 儲存電影基本資訊"""
    __tablename__ = "movies"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # TMDB Data
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    original_title = Column(String(500))
    release_date = Column(Date)
    runtime = Column(Integer)
    overview = Column(Text)
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    vote_average = Column(DECIMAL(3, 1))
    vote_count = Column(Integer)
    popularity = Column(DECIMAL(10, 3))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    genres = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")
    credits = relationship("MovieCredit", back_populates="movie", cascade="all, delete-orphan")
    moods = relationship("MovieMood", back_populates="movie", cascade="all, delete-orphan")
    embedding = relationship("MovieEmbedding", back_populates="movie", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title})>"
