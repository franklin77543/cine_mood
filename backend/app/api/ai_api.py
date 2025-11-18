"""
AI API
AI 推薦和語義搜尋的 API 端點
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.movie_repository import MovieRepository
from app.services.ai_service import get_ai_service
from app.schemas.ai_schema import (
    RecommendationRequest,
    RecommendationResponse,
    SemanticSearchRequest,
    SemanticSearchResponse,
    SimilarMoviesResponse
)

router = APIRouter(prefix="/ai", tags=["AI Recommendations"])


def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    """獲取 Movie Repository"""
    return MovieRepository(db)


@router.post("/recommend", response_model=RecommendationResponse)
def get_ai_recommendations(
    request: RecommendationRequest,
    movie_repo: MovieRepository = Depends(get_movie_repository)
):
    """
    智能推薦端點
    
    使用 LLM + Vector Search 進行智能電影推薦：
    1. 解析使用者意圖（心情、類型、關鍵字）
    2. 語義搜尋相關電影
    3. 根據意圖重排序
    4. 生成推薦理由
    
    **範例查詢**:
    - "我想看太空探險的科幻電影"
    - "輕鬆搞笑的喜劇"
    - "心情不好，想看療癒的電影"
    - "緊張刺激的動作片"
    """
    try:
        ai_service = get_ai_service(movie_repo)
        result = ai_service.get_recommendations(
            user_query=request.query,
            top_k=request.top_k,
            generate_reasons=request.generate_reasons
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推薦失敗: {str(e)}")


@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(
    request: SemanticSearchRequest,
    movie_repo: MovieRepository = Depends(get_movie_repository)
):
    """
    語義搜尋端點
    
    純向量語義搜尋，不經過 LLM 意圖解析。
    支援篩選條件：
    - `genres`: 類型列表
    - `min_rating`: 最低評分
    - `year_from`, `year_to`: 年份範圍
    
    **範例查詢**:
    - "太空探險"
    - "時間旅行"
    - "愛情故事"
    
    **範例篩選**:
    ```json
    {
        "query": "愛情",
        "filters": {
            "genres": ["科幻"],
            "min_rating": 7.0
        }
    }
    ```
    """
    try:
        ai_service = get_ai_service(movie_repo)
        result = ai_service.semantic_search(
            query=request.query,
            filters=request.filters,
            top_k=request.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜尋失敗: {str(e)}")


@router.get("/similar/{movie_id}", response_model=SimilarMoviesResponse)
def get_similar_movies(
    movie_id: str,
    top_k: int = Query(10, ge=1, le=50, description="返回數量"),
    movie_repo: MovieRepository = Depends(get_movie_repository)
):
    """
    相似電影推薦端點
    
    根據指定電影 ID，使用向量相似度找出最相似的電影。
    
    **使用情境**:
    - "喜歡這部電影，推薦類似的"
    - "更多像這樣的電影"
    """
    try:
        ai_service = get_ai_service(movie_repo)
        result = ai_service.get_similar_movies(
            movie_id=movie_id,
            top_k=top_k
        )
        
        if not result['source_movie']:
            raise HTTPException(status_code=404, detail=f"電影不存在: {movie_id}")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推薦失敗: {str(e)}")
