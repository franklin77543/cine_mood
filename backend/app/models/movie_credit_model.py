from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class MovieCredit(Base):
    """電影-演職員關聯表 - 多對多關係，區分演員與導演"""
    __tablename__ = "movie_credits"
    
    # Composite Primary Key
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), primary_key=True, index=True)
    role = Column(String(50), primary_key=True)  # 'director' or 'actor'
    
    # Additional Data
    character = Column(String(200))  # 角色名稱 (僅演員)
    order_num = Column(Integer)  # 排序 (演員順序)
    
    # Relationships
    movie = relationship("Movie", back_populates="credits")
    person = relationship("Person", back_populates="credits")
    
    def __repr__(self):
        return f"<MovieCredit(movie_id={self.movie_id}, person_id={self.person_id}, role={self.role})>"
