"""
TMDB API Client
提供與 TMDB API 互動的功能，包括獲取電影、類型、演職人員等資料
"""

import requests
import time
from typing import Optional, Dict, List, Any
from app.core.config import settings


class TMDBClient:
    """TMDB API 客戶端"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.access_token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        
        # 使用 Bearer Token 認證（較新的方式）
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # 速率限制：TMDB 免費版每秒最多 40 requests
        self.rate_limit_delay = 0.025  # 25ms between requests
        self.last_request_time = 0
    
    def _wait_for_rate_limit(self):
        """等待以符合速率限制"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        發送 API 請求
        
        Args:
            endpoint: API 端點（例如 "/movie/popular"）
            params: 查詢參數
        
        Returns:
            API 回應的 JSON 資料，失敗時返回 None
        """
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        # 默認使用繁體中文
        if params is None:
            params = {}
        if "language" not in params:
            params["language"] = "zh-TW"
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 請求失敗 [{endpoint}]: {e}")
            return None
    
    def get_genres(self) -> List[Dict[str, Any]]:
        """
        獲取所有電影類型
        
        Returns:
            類型列表，每個類型包含 id 和 name
        """
        data = self._make_request("/genre/movie/list")
        if data and "genres" in data:
            return data["genres"]
        return []
    
    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """
        獲取熱門電影列表
        
        Args:
            page: 頁碼（1-500）
        
        Returns:
            包含電影列表和分頁資訊的字典
        """
        return self._make_request("/movie/popular", {"page": page})
    
    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict]:
        """
        獲取高評分電影列表
        
        Args:
            page: 頁碼（1-500）
        
        Returns:
            包含電影列表和分頁資訊的字典
        """
        return self._make_request("/movie/top_rated", {"page": page})
    
    def get_now_playing_movies(self, page: int = 1) -> Optional[Dict]:
        """
        獲取正在上映的電影
        
        Args:
            page: 頁碼（1-500）
        
        Returns:
            包含電影列表和分頁資訊的字典
        """
        return self._make_request("/movie/now_playing", {"page": page})
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """
        獲取電影詳細資料
        
        Args:
            movie_id: TMDB 電影 ID
        
        Returns:
            電影詳細資訊
        """
        return self._make_request(f"/movie/{movie_id}")
    
    def get_movie_credits(self, movie_id: int) -> Optional[Dict]:
        """
        獲取電影演職人員資料
        
        Args:
            movie_id: TMDB 電影 ID
        
        Returns:
            包含 cast（演員）和 crew（工作人員）的字典
        """
        return self._make_request(f"/movie/{movie_id}/credits")
    
    def get_image_url(self, path: str, size: str = "original") -> str:
        """
        構建完整的圖片 URL
        
        Args:
            path: 圖片路徑（例如 "/abc123.jpg"）
            size: 圖片尺寸（w500, original 等）
        
        Returns:
            完整圖片 URL
        """
        if not path:
            return ""
        return f"{self.image_base_url}/{size}{path}"
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """
        搜尋電影
        
        Args:
            query: 搜尋關鍵字
            page: 頁碼
        
        Returns:
            搜尋結果
        """
        return self._make_request("/search/movie", {"query": query, "page": page})


# 單例實例
tmdb_client = TMDBClient()
