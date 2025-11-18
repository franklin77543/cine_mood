from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class MoodTag(Base):
    """情緒標籤表 - 儲存預定義的情緒標籤"""
    __tablename__ = "mood_tags"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Data
    tag = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    movies = relationship("MovieMood", back_populates="mood_tag")
    
    def __repr__(self):
        return f"<MoodTag(id={self.id}, tag={self.tag})>"
