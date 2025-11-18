"""
Test AI API Endpoints
測試 AI API 的三個端點
"""
import requests
import json
import sys
import os
from pathlib import Path

# 設置工作目錄
backend_dir = Path(__file__).parent.parent
os.chdir(backend_dir)

BASE_URL = "http://localhost:8000/api/v1"


def print_section(title):
    """打印分隔線"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_recommend_endpoint():
    """測試智能推薦端點"""
    print_section("測試 1: POST /ai/recommend - 智能推薦")
    
    test_cases = [
        {
            "query": "我想看太空探險的科幻電影",
            "top_k": 5,
            "generate_reasons": True
        },
        {
            "query": "輕鬆搞笑的喜劇",
            "top_k": 3,
            "generate_reasons": True
        },
        {
            "query": "心情不好，想看療癒感人的電影",
            "top_k": 5,
            "generate_reasons": True
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 測試案例 {i}")
        print(f"查詢: '{case['query']}'")
        print("-" * 80)
        
        response = requests.post(
            f"{BASE_URL}/ai/recommend",
            json=case
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✅ 請求成功!")
            print(f"\n意圖解析:")
            intent = data['intent']
            print(f"  心情: {intent.get('mood')}")
            print(f"  類型: {intent.get('genres')}")
            print(f"  關鍵字: {intent.get('keywords')}")
            
            print(f"\n推薦結果 (共 {data['total']} 部):")
            for j, rec in enumerate(data['recommendations'], 1):
                print(f"\n  {j}. {rec['title']}")
                print(f"     類型: {', '.join(rec['genres'])}")
                print(f"     相似度: {rec['similarity_score']:.3f}")
                if rec.get('vote_average'):
                    print(f"     評分: {rec['vote_average']}")
                if rec.get('reason'):
                    print(f"     推薦理由: {rec['reason']}")
        else:
            print(f"❌ 請求失敗: {response.status_code}")
            print(response.text)


def test_search_endpoint():
    """測試語義搜尋端點"""
    print_section("測試 2: POST /ai/search - 語義搜尋")
    
    # 測試案例 1: 無篩選
    print("\n📝 測試案例 1: 無篩選")
    print("查詢: '時間旅行'")
    print("-" * 80)
    
    response = requests.post(
        f"{BASE_URL}/ai/search",
        json={
            "query": "時間旅行",
            "top_k": 5
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ 找到 {data['total']} 部相關電影:")
        for i, result in enumerate(data['results'], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     類型: {', '.join(result['genres'])}")
            print(f"     相似度: {result['similarity_score']:.3f}")
    else:
        print(f"❌ 請求失敗: {response.status_code}")
    
    # 測試案例 2: 有篩選
    print("\n\n📝 測試案例 2: 類型篩選 + 評分篩選")
    print("查詢: '愛情' (科幻類型, 評分 >= 6.0)")
    print("-" * 80)
    
    response = requests.post(
        f"{BASE_URL}/ai/search",
        json={
            "query": "愛情",
            "top_k": 5,
            "filters": {
                "genres": ["科幻"],
                "min_rating": 6.0
            }
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ 找到 {data['total']} 部符合條件的電影:")
        for i, result in enumerate(data['results'], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     類型: {', '.join(result['genres'])}")
            print(f"     相似度: {result['similarity_score']:.3f}")
    else:
        print(f"❌ 請求失敗: {response.status_code}")


def test_similar_endpoint():
    """測試相似電影端點"""
    print_section("測試 3: GET /ai/similar/{movie_id} - 相似電影")
    
    # 先獲取一部電影的 ID
    print("\n📝 先獲取一部電影...")
    response = requests.get(f"{BASE_URL}/movies?limit=1")
    
    if response.status_code == 200:
        movies = response.json()['movies']
        if movies:
            test_movie = movies[0]
            movie_id = test_movie['id']
            movie_title = test_movie['title']
            
            print(f"使用電影: {movie_title} (ID: {movie_id})")
            print("-" * 80)
            
            # 獲取相似電影
            response = requests.get(
                f"{BASE_URL}/ai/similar/{movie_id}",
                params={"top_k": 5}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n✅ 基於電影: {data['source_movie']['title']}")
                print(f"   類型: {', '.join(data['source_movie']['genres'])}")
                
                print(f"\n找到 {data['total']} 部相似電影:")
                for i, similar in enumerate(data['similar_movies'], 1):
                    print(f"\n  {i}. {similar['title']}")
                    print(f"     類型: {', '.join(similar['genres'])}")
                    print(f"     相似度: {similar['similarity_score']:.3f}")
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                print(response.text)
    else:
        print(f"❌ 無法獲取電影列表: {response.status_code}")


def main():
    """執行所有測試"""
    print("=" * 80)
    print("  AI API 端點測試")
    print("  Server: http://localhost:8000")
    print("=" * 80)
    
    try:
        # 檢查服務器是否運行
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            print(f"\n✅ 服務器運行中 (status: {response.status_code})\n")
        except requests.exceptions.RequestException as e:
            print(f"❌ 無法連接到服務器: {e}")
            print("請確認 FastAPI 服務器正在運行於 http://localhost:8000")
            return
        
        # 執行測試
        test_recommend_endpoint()
        test_search_endpoint()
        test_similar_endpoint()
        
        print("\n\n" + "=" * 80)
        print("  ✅ 所有 API 測試完成!")
        print("=" * 80)
        print(f"\n📚 API 文檔: http://localhost:8000/docs")
        print(f"📖 ReDoc: http://localhost:8000/redoc\n")
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器，請確認 FastAPI 服務器正在運行")
        print("   啟動命令: uvicorn app.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")


if __name__ == '__main__':
    main()
