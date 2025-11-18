"""
Movie API Endpoints
電影相關的 RESTful API
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.dependencies import get_movie_service
from app.services.movie_service import MovieService
from app.schemas.movie_schema import MovieDetail, MovieListResponse


router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=MovieListResponse)
def get_movies(
    page: int = Query(1, ge=1, description="頁碼"),
    page_size: int = Query(20, ge=1, le=100, description="每頁數量"),
    genre_id: Optional[int] = Query(None, description="類型 ID（可選）"),
    service: MovieService = Depends(get_movie_service)
):
    """
    獲取電影列表
    
    - **page**: 頁碼（從 1 開始）
    - **page_size**: 每頁數量（1-100）
    - **genre_id**: 可選，按類型篩選
    """
    return service.list_movies(page=page, page_size=page_size, genre_id=genre_id)


@router.get("/search", response_model=MovieListResponse)
def search_movies(
    q: str = Query(..., min_length=1, description="搜尋關鍵字"),
    page: int = Query(1, ge=1, description="頁碼"),
    page_size: int = Query(20, ge=1, le=100, description="每頁數量"),
    service: MovieService = Depends(get_movie_service)
):
    """
    搜尋電影（支援中文）
    
    - **q**: 搜尋關鍵字（必填）
    - **page**: 頁碼（從 1 開始）
    - **page_size**: 每頁數量（1-100）
    """
    return service.search_movies(query=q, page=page, page_size=page_size)


@router.get("/{movie_id}", response_model=MovieDetail)
def get_movie_detail(
    movie_id: str,
    service: MovieService = Depends(get_movie_service)
):
    """
    獲取電影詳細資訊
    
    - **movie_id**: 電影 UUID
    """
    return service.get_movie_detail(movie_id)
