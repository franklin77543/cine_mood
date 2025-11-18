from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime


class MovieEmbedding(Base):
    """電影向量表 - 一對一關係，用於語義搜尋"""
    __tablename__ = "movie_embeddings"
    
    # Primary Key (Foreign Key to movies)
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    
    # Embedding Data
    embedding = Column(Text, nullable=False)  # JSON string of vector (384 dimensions)
    embedding_text = Column(Text)  # 用於生成向量的原始文本
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    movie = relationship("Movie", back_populates="embedding")
    
    def __repr__(self):
        return f"<MovieEmbedding(movie_id={self.movie_id})>"
