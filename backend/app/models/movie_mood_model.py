from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class MovieMood(Base):
    """電影-情緒標籤關聯表 - 多對多關係，帶權重"""
    __tablename__ = "movie_moods"
    
    # Composite Primary Key
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    mood_id = Column(Integer, ForeignKey("mood_tags.id", ondelete="CASCADE"), primary_key=True, index=True)
    
    # Weight (0-1)
    weight = Column(DECIMAL(3, 2))  # 關聯強度
    
    # Relationships
    movie = relationship("Movie", back_populates="moods")
    mood_tag = relationship("MoodTag", back_populates="movies")
    
    def __repr__(self):
        return f"<MovieMood(movie_id={self.movie_id}, mood_id={self.mood_id}, weight={self.weight})>"
