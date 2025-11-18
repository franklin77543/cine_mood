"""
API 端點測試腳本
測試所有 Phase 2 實現的 API
"""
import requests
import json
from typing import Dict, Any


BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"


def print_response(title: str, response: requests.Response):
    """格式化輸出回應"""
    print(f"\n{'='*60}")
    print(f"✅ {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_health():
    """測試健康檢查"""
    response = requests.get(f"{API_V1}/health")
    print_response("Health Check", response)


def test_genres():
    """測試獲取所有類型"""
    response = requests.get(f"{API_V1}/genres")
    print_response("Get All Genres", response)
    return response.json() if response.status_code == 200 else []


def test_movies_list():
    """測試電影列表"""
    response = requests.get(f"{API_V1}/movies?page=1&page_size=5")
    print_response("Get Movies List (Page 1, Size 5)", response)
    return response.json() if response.status_code == 200 else None


def test_movie_detail(movie_id: str):
    """測試電影詳情"""
    response = requests.get(f"{API_V1}/movies/{movie_id}")
    print_response(f"Get Movie Detail (ID: {movie_id})", response)


def test_search_movies(query: str):
    """測試電影搜尋"""
    response = requests.get(f"{API_V1}/movies/search?q={query}&page=1&page_size=5")
    print_response(f"Search Movies (Query: '{query}')", response)


def test_movies_by_genre(genre_id: int):
    """測試按類型篩選電影"""
    response = requests.get(f"{API_V1}/movies?genre_id={genre_id}&page=1&page_size=5")
    print_response(f"Get Movies by Genre (Genre ID: {genre_id})", response)


def main():
    print("\n" + "🎬" * 30)
    print("CineMood API 測試開始")
    print("🎬" * 30)
    
    try:
        # 1. 健康檢查
        test_health()
        
        # 2. 獲取所有類型
        genres = test_genres()
        
        # 3. 獲取電影列表
        movies_data = test_movies_list()
        
        # 4. 測試電影詳情（使用列表中第一部電影）
        if movies_data and movies_data.get("movies"):
            first_movie = movies_data["movies"][0]
            test_movie_detail(first_movie["id"])
        
        # 5. 測試搜尋（中文）
        test_search_movies("科學")
        
        # 6. 測試按類型篩選（使用第一個類型）
        if genres and len(genres) > 0:
            test_movies_by_genre(genres[0]["id"])
        
        print("\n" + "✅" * 30)
        print("所有測試完成！")
        print("✅" * 30 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 錯誤：無法連接到 API 伺服器")
        print("請確認伺服器正在運行於 http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤：{str(e)}")


if __name__ == "__main__":
    main()
