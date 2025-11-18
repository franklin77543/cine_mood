from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class MovieGenre(Base):
    """電影-類型關聯表 - 多對多關係"""
    __tablename__ = "movie_genres"
    
    # Composite Primary Key
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True, index=True)
    
    # Relationships
    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movies")
    
    def __repr__(self):
        return f"<MovieGenre(movie_id={self.movie_id}, genre_id={self.genre_id})>"
