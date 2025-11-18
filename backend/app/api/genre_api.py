"""
Genre API Endpoints
電影類型相關的 RESTful API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.services.genre_service import GenreService
from app.schemas.genre_schema import GenreSchema


router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("", response_model=List[GenreSchema])
def get_all_genres(db: Session = Depends(get_db)):
    """
    獲取所有電影類型
    
    返回資料庫中所有可用的電影類型列表
    """
    service = GenreService(db)
    return service.get_all_genres()
