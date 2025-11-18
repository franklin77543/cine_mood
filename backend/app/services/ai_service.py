"""
AI Service
整合 LLM + Embedding + Vector Search 的智能推薦服務
"""
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
import numpy as np
import logging

from app.services.embedding_service import get_embedding_service
from app.services.vector_store import get_vector_store
from app.services.llm_service import get_llm_service
from app.repositories.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


class AIService:
    """AI 推薦服務 - 混合檢索與智能推薦"""
    
    def __init__(self, movie_repository: MovieRepository):
        """
        初始化 AI 服務
        
        Args:
            movie_repository: 電影資料庫
        """
        self.movie_repo = movie_repository
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
        self.llm_service = get_llm_service()
        
        # 載入向量存儲（如果尚未載入）
        if len(self.vector_store) == 0:
            from pathlib import Path
            store_path = Path(__file__).parent.parent.parent / 'data' / 'vector_store.pkl'
            if store_path.exists():
                self.vector_store.load(str(store_path))
                logger.info(f"Loaded {len(self.vector_store)} vectors from store")
    
    def get_recommendations(
        self, 
        user_query: str, 
        top_k: int = 10,
        generate_reasons: bool = True
    ) -> Dict:
        """
        智能推薦主流程
        
        Args:
            user_query: 使用者查詢
            top_k: 返回推薦數量
            generate_reasons: 是否生成推薦理由
            
        Returns:
            {
                "query": str,
                "intent": Dict,
                "recommendations": List[Dict],
                "total": int
            }
        """
        logger.info(f"Processing recommendation request: {user_query}")
        
        # 1. LLM 解析使用者意圖
        intent = self.llm_service.parse_user_intent(user_query)
        logger.info(f"Parsed intent: {intent}")
        
        # 2. 生成查詢向量
        query_embedding = self.embedding_service.encode_text(user_query)
        
        # 3. 向量搜尋（取 top_k * 2 以便後續篩選）
        search_k = min(top_k * 2, len(self.vector_store))
        vector_results = self.vector_store.search(
            query_embedding, 
            top_k=search_k
        )
        
        # 4. Metadata 篩選和重排序
        filtered_results = self._filter_and_rerank(
            vector_results, 
            intent
        )
        
        # 5. 取 top_k
        top_results = filtered_results[:top_k]
        
        # 6. 組裝推薦結果
        recommendations = []
        for movie_id, similarity, metadata in top_results:
            # 從資料庫獲取完整電影資訊
            movie = self.movie_repo.get_movie_by_id(movie_id)
            
            if movie:
                rec_item = {
                    "movie_id": movie_id,
                    "title": metadata['title'],
                    "genres": metadata['genres'],
                    "overview": metadata.get('overview'),
                    "release_date": metadata.get('release_date'),
                    "poster_path": metadata.get('poster_path'),
                    "backdrop_path": metadata.get('backdrop_path'),
                    "vote_average": metadata.get('vote_average'),
                    "popularity": metadata.get('popularity'),
                    "similarity_score": round(similarity, 3),
                    "reason": None
                }
                
                # 生成推薦理由（可選）
                if generate_reasons:
                    reason = self.llm_service.generate_recommendation_reason(
                        movie_title=metadata['title'],
                        movie_overview=metadata.get('overview', ''),
                        movie_genres=metadata['genres'],
                        user_query=user_query
                    )
                    rec_item['reason'] = reason
                
                recommendations.append(rec_item)
        
        return {
            "query": user_query,
            "intent": intent,
            "recommendations": recommendations,
            "total": len(recommendations)
        }
    
    def semantic_search(
        self, 
        query: str, 
        filters: Optional[Dict] = None,
        top_k: int = 10
    ) -> Dict:
        """
        純語義搜尋（不經過 LLM）
        
        Args:
            query: 查詢文本
            filters: 篩選條件 {"genres": [...], "min_rating": float}
            top_k: 返回數量
            
        Returns:
            {
                "query": str,
                "results": List[Dict],
                "total": int
            }
        """
        logger.info(f"Processing semantic search: {query}")
        
        # 生成查詢向量
        query_embedding = self.embedding_service.encode_text(query)
        
        # 類型篩選
        filter_genre = None
        if filters and 'genres' in filters and filters['genres']:
            filter_genre = filters['genres'][0]  # 目前只支援單一類型篩選
        
        # 向量搜尋
        vector_results = self.vector_store.search(
            query_embedding, 
            top_k=top_k * 2 if filters else top_k,
            filter_genre=filter_genre
        )
        
        # 應用其他篩選條件
        filtered_results = vector_results
        if filters:
            filtered_results = self._apply_filters(vector_results, filters)
        
        # 取 top_k
        top_results = filtered_results[:top_k]
        
        # 組裝結果
        results = []
        for movie_id, similarity, metadata in top_results:
            results.append({
                "movie_id": movie_id,
                "title": metadata['title'],
                "genres": metadata['genres'],
                "overview": metadata.get('overview'),
                "poster_path": metadata.get('poster_path'),
                "backdrop_path": metadata.get('backdrop_path'),
                "similarity_score": round(similarity, 3)
            })
        
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    
    def get_similar_movies(
        self, 
        movie_id: str, 
        top_k: int = 10
    ) -> Dict:
        """
        根據電影找相似電影
        
        Args:
            movie_id: 電影 ID
            top_k: 返回數量
            
        Returns:
            {
                "source_movie": Dict,
                "similar_movies": List[Dict],
                "total": int
            }
        """
        logger.info(f"Finding similar movies for: {movie_id}")
        
        # 從向量存儲獲取電影向量
        result = self.vector_store.get_by_movie_id(movie_id)
        
        if not result:
            logger.warning(f"Movie not found in vector store: {movie_id}")
            return {
                "source_movie": None,
                "similar_movies": [],
                "total": 0
            }
        
        vector, metadata = result
        
        # 搜尋相似電影（top_k + 1 因為第一個是自己）
        similar_results = self.vector_store.search(
            vector, 
            top_k=top_k + 1
        )
        
        # 移除自己
        similar_results = [
            (mid, sim, meta) 
            for mid, sim, meta in similar_results 
            if mid != movie_id
        ][:top_k]
        
        # 組裝結果
        similar_movies = []
        for mid, similarity, meta in similar_results:
            similar_movies.append({
                "movie_id": mid,
                "title": meta['title'],
                "genres": meta['genres'],
                "overview": meta.get('overview'),
                "poster_path": meta.get('poster_path'),
                "backdrop_path": meta.get('backdrop_path'),
                "similarity_score": round(similarity, 3)
            })
        
        return {
            "source_movie": {
                "movie_id": movie_id,
                "title": metadata['title'],
                "genres": metadata['genres']
            },
            "similar_movies": similar_movies,
            "total": len(similar_movies)
        }
    
    def _filter_and_rerank(
        self, 
        vector_results: List[Tuple[str, float, Dict]], 
        intent: Dict
    ) -> List[Tuple[str, float, Dict]]:
        """
        根據意圖篩選和重排序結果
        
        Args:
            vector_results: 向量搜尋結果
            intent: 使用者意圖
            
        Returns:
            篩選和重排序後的結果
        """
        results = []
        
        for movie_id, similarity, metadata in vector_results:
            # 計算匹配分數
            match_score = similarity
            
            # 類型匹配加分
            if intent.get('genres'):
                movie_genres = set(metadata['genres'])
                intent_genres = set(intent['genres'])
                genre_overlap = len(movie_genres & intent_genres)
                
                if genre_overlap > 0:
                    # 類型匹配，提高分數
                    match_score += 0.1 * genre_overlap
            
            # 關鍵字匹配加分
            if intent.get('keywords'):
                overview = metadata.get('overview', '').lower()
                title = metadata['title'].lower()
                
                keyword_matches = sum(
                    1 for kw in intent['keywords'] 
                    if kw.lower() in overview or kw.lower() in title
                )
                
                if keyword_matches > 0:
                    match_score += 0.05 * keyword_matches
            
            results.append((movie_id, match_score, metadata))
        
        # 按匹配分數降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def _apply_filters(
        self, 
        results: List[Tuple[str, float, Dict]], 
        filters: Dict
    ) -> List[Tuple[str, float, Dict]]:
        """
        應用篩選條件
        
        Args:
            results: 搜尋結果
            filters: 篩選條件
            
        Returns:
            篩選後的結果
        """
        filtered = results
        
        # 最低評分篩選
        if 'min_rating' in filters:
            min_rating = filters['min_rating']
            filtered = [
                (mid, sim, meta) 
                for mid, sim, meta in filtered 
                if meta.get('vote_average', 0) >= min_rating
            ]
        
        # 年份範圍篩選
        if 'year_from' in filters or 'year_to' in filters:
            year_from = filters.get('year_from', 1900)
            year_to = filters.get('year_to', 2100)
            
            filtered = [
                (mid, sim, meta) 
                for mid, sim, meta in filtered 
                if meta.get('release_date') and 
                   year_from <= int(meta['release_date'][:4]) <= year_to
            ]
        
        return filtered


def get_ai_service(movie_repository: MovieRepository) -> AIService:
    """
    獲取 AI Service 實例
    
    Args:
        movie_repository: 電影資料庫
        
    Returns:
        AIService 實例
    """
    return AIService(movie_repository)
