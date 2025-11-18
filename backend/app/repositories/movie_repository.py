"""
Movie Repository
負責電影相關的資料庫操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.models.movie_model import Movie
from app.models.movie_genre_model import MovieGenre
from app.models.movie_credit_model import MovieCredit


class MovieRepository:
    """電影資料存取層"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_movie_by_id(self, movie_id: str) -> Optional[Movie]:
        """
        根據 ID 獲取電影詳細資訊
        使用 joinedload 預載關聯資料，避免 N+1 查詢問題
        """
        return (
            self.db.query(Movie)
            .options(
                joinedload(Movie.genres).joinedload(MovieGenre.genre),
                joinedload(Movie.credits).joinedload(MovieCredit.person)
            )
            .filter(Movie.id == movie_id)
            .first()
        )
    
    def get_movies(self, skip: int = 0, limit: int = 20) -> List[Movie]:
        """
        獲取電影列表（分頁）
        按照人氣度排序
        """
        return (
            self.db.query(Movie)
            .options(
                joinedload(Movie.genres).joinedload(MovieGenre.genre)
            )
            .order_by(Movie.popularity.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_total_count(self) -> int:
        """獲取電影總數"""
        return self.db.query(func.count(Movie.id)).scalar()
    
    def search_movies(self, query: str, skip: int = 0, limit: int = 20) -> List[Movie]:
        """
        搜尋電影（支援中文）
        在 title 和 original_title 中搜尋
        """
        search_pattern = f"%{query}%"
        return (
            self.db.query(Movie)
            .options(
                joinedload(Movie.genres).joinedload(MovieGenre.genre)
            )
            .filter(
                or_(
                    Movie.title.like(search_pattern),
                    Movie.original_title.like(search_pattern),
                    Movie.overview.like(search_pattern)
                )
            )
            .order_by(Movie.popularity.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_count(self, query: str) -> int:
        """獲取搜尋結果總數"""
        search_pattern = f"%{query}%"
        return (
            self.db.query(func.count(Movie.id))
            .filter(
                or_(
                    Movie.title.like(search_pattern),
                    Movie.original_title.like(search_pattern),
                    Movie.overview.like(search_pattern)
                )
            )
            .scalar()
        )
    
    def get_movies_by_genre(self, genre_id: int, skip: int = 0, limit: int = 20) -> List[Movie]:
        """根據類型獲取電影"""
        return (
            self.db.query(Movie)
            .join(Movie.genres)
            .filter(MovieGenre.genre_id == genre_id)
            .options(
                joinedload(Movie.genres).joinedload(MovieGenre.genre)
            )
            .order_by(Movie.popularity.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
