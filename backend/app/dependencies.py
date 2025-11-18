"""
Dependencies
FastAPI 依賴注入
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.movie_repository import MovieRepository
from app.repositories.genre_repository import GenreRepository
from app.repositories.health_repository import HealthRepository
from app.services.movie_service import MovieService
from app.services.genre_service import GenreService
from app.services.health_service import HealthService


def get_db() -> Generator:
    """
    獲取資料庫 Session
    使用 FastAPI 依賴注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Repository Dependencies
def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    """獲取 Movie Repository"""
    return MovieRepository(db)


def get_genre_repository(db: Session = Depends(get_db)) -> GenreRepository:
    """獲取 Genre Repository"""
    return GenreRepository(db)


def get_health_repository(db: Session = Depends(get_db)) -> HealthRepository:
    """獲取 Health Repository"""
    return HealthRepository(db)


# Service Dependencies
def get_movie_service(
    movie_repo: MovieRepository = Depends(get_movie_repository),
    genre_repo: GenreRepository = Depends(get_genre_repository)
) -> MovieService:
    """獲取 Movie Service"""
    return MovieService(movie_repo, genre_repo)


def get_genre_service(
    genre_repo: GenreRepository = Depends(get_genre_repository)
) -> GenreService:
    """獲取 Genre Service"""
    return GenreService(genre_repo)


def get_health_service(
    health_repo: HealthRepository = Depends(get_health_repository)
) -> HealthService:
    """獲取 Health Service"""
    return HealthService(health_repo)
