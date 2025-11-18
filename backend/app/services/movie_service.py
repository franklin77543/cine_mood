"""
Movie Service
電影相關業務邏輯
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import math

from app.repositories.movie_repository import MovieRepository
from app.repositories.genre_repository import GenreRepository
from app.schemas.movie_schema import MovieDetail, MovieListItem, MovieListResponse


class MovieService:
    """電影業務邏輯層"""
    
    def __init__(self, db: Session):
        self.movie_repo = MovieRepository(db)
        self.genre_repo = GenreRepository(db)
    
    def get_movie_detail(self, movie_id: str) -> MovieDetail:
        """
        獲取電影詳細資訊
        如果找不到，拋出 404 錯誤
        """
        movie = self.movie_repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")
        
        return MovieDetail.from_orm_movie(movie)
    
    def list_movies(self, page: int = 1, page_size: int = 20, genre_id: Optional[int] = None) -> MovieListResponse:
        """
        獲取電影列表（分頁）
        可選擇按類型篩選
        """
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20
        
        skip = (page - 1) * page_size
        
        # 根據是否有 genre_id 選擇不同的查詢方法
        if genre_id:
            # 驗證 genre 是否存在
            genre = self.genre_repo.get_genre_by_id(genre_id)
            if not genre:
                raise HTTPException(status_code=404, detail=f"Genre with id {genre_id} not found")
            
            movies = self.movie_repo.get_movies_by_genre(genre_id, skip, limit=page_size)
            # TODO: 需要在 repository 中增加 get_movies_by_genre_count 方法
            total = len(movies)  # 暫時使用這個，後續優化
        else:
            movies = self.movie_repo.get_movies(skip, limit=page_size)
            total = self.movie_repo.get_total_count()
        
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        movie_items = [MovieListItem.from_orm_movie(movie) for movie in movies]
        
        return MovieListResponse(
            movies=movie_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def search_movies(self, query: str, page: int = 1, page_size: int = 20) -> MovieListResponse:
        """
        搜尋電影（支援中文）
        """
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20
        
        skip = (page - 1) * page_size
        
        movies = self.movie_repo.search_movies(query, skip, limit=page_size)
        total = self.movie_repo.search_count(query)
        
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        movie_items = [MovieListItem.from_orm_movie(movie) for movie in movies]
        
        return MovieListResponse(
            movies=movie_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
