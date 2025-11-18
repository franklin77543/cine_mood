from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class Genre(Base):
    """類型表 - 儲存電影類型 (動作、喜劇、劇情等)"""
    __tablename__ = "genres"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # TMDB Data
    tmdb_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    movies = relationship("MovieGenre", back_populates="genre")
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name={self.name})>"
