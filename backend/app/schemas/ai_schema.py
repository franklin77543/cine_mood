"""
AI Schemas
AI 推薦相關的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date


class UserIntent(BaseModel):
    """使用者意圖"""
    mood: Optional[str] = None
    genres: List[str] = []
    keywords: List[str] = []
    preferences: Dict = {}


class RecommendationRequest(BaseModel):
    """推薦請求"""
    query: str = Field(..., description="使用者查詢", min_length=1)
    top_k: int = Field(10, description="返回推薦數量", ge=1, le=50)
    generate_reasons: bool = Field(True, description="是否生成推薦理由")


class MovieRecommendation(BaseModel):
    """推薦的電影"""
    movie_id: str
    title: str
    genres: List[str]
    overview: Optional[str] = None
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    vote_average: Optional[float] = None
    popularity: Optional[float] = None
    similarity_score: float
    reason: Optional[str] = None


class RecommendationResponse(BaseModel):
    """推薦響應"""
    query: str
    intent: UserIntent
    recommendations: List[MovieRecommendation]
    total: int


class SemanticSearchRequest(BaseModel):
    """語義搜尋請求"""
    query: str = Field(..., description="搜尋查詢", min_length=1)
    top_k: int = Field(10, description="返回數量", ge=1, le=50)
    filters: Optional[Dict] = Field(None, description="篩選條件")


class SearchResult(BaseModel):
    """搜尋結果"""
    movie_id: str
    title: str
    genres: List[str]
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    similarity_score: float


class SemanticSearchResponse(BaseModel):
    """語義搜尋響應"""
    query: str
    results: List[SearchResult]
    total: int


class SimilarMovieItem(BaseModel):
    """相似電影項目"""
    movie_id: str
    title: str
    genres: List[str]
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    similarity_score: float


class SourceMovie(BaseModel):
    """源電影"""
    movie_id: str
    title: str
    genres: List[str]


class SimilarMoviesResponse(BaseModel):
    """相似電影響應"""
    source_movie: Optional[SourceMovie]
    similar_movies: List[SimilarMovieItem]
    total: int
