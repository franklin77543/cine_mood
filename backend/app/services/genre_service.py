"""
Genre Service
電影類型業務邏輯
"""
from typing import List
from sqlalchemy.orm import Session

from app.repositories.genre_repository import GenreRepository
from app.schemas.genre_schema import GenreSchema


class GenreService:
    """電影類型業務邏輯層"""
    
    def __init__(self, db: Session):
        self.genre_repo = GenreRepository(db)
    
    def get_all_genres(self) -> List[GenreSchema]:
        """獲取所有電影類型"""
        genres = self.genre_repo.get_all_genres()
        return [GenreSchema.model_validate(genre) for genre in genres]
