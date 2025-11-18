from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid


class Person(Base):
    """演職員表 - 儲存演員、導演等人員資訊"""
    __tablename__ = "people"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # TMDB Data
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    profile_path = Column(String(500))
    
    # Relationships
    credits = relationship("MovieCredit", back_populates="person")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name={self.name})>"
