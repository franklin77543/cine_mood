"""
Genre Repository
負責電影類型相關的資料庫操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.genre_model import Genre


class GenreRepository:
    """電影類型資料存取層"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_genres(self) -> List[Genre]:
        """獲取所有電影類型"""
        return self.db.query(Genre).order_by(Genre.name).all()
    
    def get_genre_by_id(self, genre_id: int) -> Optional[Genre]:
        """根據 ID 獲取類型"""
        return self.db.query(Genre).filter(Genre.id == genre_id).first()
    
    def get_genre_by_tmdb_id(self, tmdb_id: int) -> Optional[Genre]:
        """根據 TMDB ID 獲取類型"""
        return self.db.query(Genre).filter(Genre.tmdb_id == tmdb_id).first()
