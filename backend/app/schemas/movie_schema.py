"""
Movie Schemas
電影的 Pydantic 模型
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from app.schemas.genre_schema import GenreSchema
from app.schemas.person_schema import CreditSchema


class MovieBase(BaseModel):
    """Movie 基礎模型"""
    id: str
    tmdb_id: int
    title: str
    original_title: str
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class MovieListItem(MovieBase):
    """電影列表項目（包含類型）"""
    genres: List[GenreSchema] = []
    
    @classmethod
    def from_orm_movie(cls, movie):
        """從 ORM Movie 物件轉換"""
        genres = [GenreSchema.model_validate(mg.genre) for mg in movie.genres]
        data = {
            "id": movie.id,
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "original_title": movie.original_title,
            "release_date": movie.release_date,
            "vote_average": movie.vote_average,
            "popularity": movie.popularity,
            "poster_path": movie.poster_path,
            "genres": genres
        }
        return cls(**data)


class MovieDetail(MovieBase):
    """電影詳細資訊（包含類型、演職人員）"""
    overview: Optional[str] = None
    runtime: Optional[int] = None
    vote_count: Optional[int] = None
    backdrop_path: Optional[str] = None
    genres: List[GenreSchema] = []
    credits: List[CreditSchema] = []
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_orm_movie(cls, movie):
        """從 ORM Movie 物件轉換"""
        genres = [GenreSchema.model_validate(mg.genre) for mg in movie.genres]
        credits = [
            CreditSchema(
                person=mc.person,
                role=mc.role,
                character=mc.character,
                order_num=mc.order_num
            )
            for mc in sorted(movie.credits, key=lambda x: (x.role != 'director', x.order_num or 999))
        ]
        
        data = {
            "id": movie.id,
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "original_title": movie.original_title,
            "overview": movie.overview,
            "release_date": movie.release_date,
            "runtime": movie.runtime,
            "vote_average": movie.vote_average,
            "vote_count": movie.vote_count,
            "popularity": movie.popularity,
            "poster_path": movie.poster_path,
            "backdrop_path": movie.backdrop_path,
            "genres": genres,
            "credits": credits,
            "created_at": movie.created_at,
            "updated_at": movie.updated_at
        }
        return cls(**data)


class MovieListResponse(BaseModel):
    """電影列表回應（帶分頁資訊）"""
    movies: List[MovieListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    model_config = ConfigDict(from_attributes=True)
