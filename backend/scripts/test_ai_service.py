"""
Test AI Service
測試完整的 AI 推薦服務
"""
import sys
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.repositories.movie_repository import MovieRepository
from app.services.ai_service import get_ai_service


def test_ai_service():
    """測試 AI 推薦服務"""
    print("Testing AI Service - Full Integration")
    print("=" * 80)
    
    # 初始化
    db = SessionLocal()
    movie_repo = MovieRepository(db)
    ai_service = get_ai_service(movie_repo)
    
    try:
        # 測試 1: 智能推薦
        print("\n🎬 測試 1: 智能推薦 (get_recommendations)")
        print("-" * 80)
        
        queries = [
            "我想看太空探險的科幻電影",
            "輕鬆搞笑的喜劇",
            "心情不好，想看療癒感人的電影"
        ]
        
        for query in queries:
            print(f"\n查詢: '{query}'")
            result = ai_service.get_recommendations(
                user_query=query,
                top_k=5,
                generate_reasons=True
            )
            
            print(f"\n意圖解析:")
            print(f"  心情: {result['intent'].get('mood')}")
            print(f"  類型: {result['intent'].get('genres')}")
            print(f"  關鍵字: {result['intent'].get('keywords')}")
            
            print(f"\n推薦結果 (共 {result['total']} 部):")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"\n  {i}. {rec['title']}")
                print(f"     類型: {', '.join(rec['genres'])}")
                print(f"     相似度: {rec['similarity_score']:.3f}")
                if rec.get('vote_average'):
                    print(f"     評分: {rec['vote_average']}")
                if rec.get('reason'):
                    print(f"     推薦理由: {rec['reason']}")
        
        # 測試 2: 語義搜尋
        print("\n\n" + "=" * 80)
        print("🔍 測試 2: 語義搜尋 (semantic_search)")
        print("-" * 80)
        
        search_query = "時間旅行"
        print(f"\n查詢: '{search_query}'")
        
        result = ai_service.semantic_search(
            query=search_query,
            top_k=5
        )
        
        print(f"\n找到 {result['total']} 部相關電影:")
        for i, item in enumerate(result['results'], 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     類型: {', '.join(item['genres'])}")
            print(f"     相似度: {item['similarity_score']:.3f}")
        
        # 測試 3: 語義搜尋 + 篩選
        print("\n\n" + "=" * 80)
        print("🎯 測試 3: 語義搜尋 + 篩選")
        print("-" * 80)
        
        search_query = "愛情"
        filters = {
            "genres": ["科幻"],
            "min_rating": 6.0
        }
        
        print(f"\n查詢: '{search_query}'")
        print(f"篩選: 類型={filters['genres']}, 最低評分={filters['min_rating']}")
        
        result = ai_service.semantic_search(
            query=search_query,
            filters=filters,
            top_k=5
        )
        
        print(f"\n找到 {result['total']} 部符合條件的電影:")
        for i, item in enumerate(result['results'], 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     類型: {', '.join(item['genres'])}")
            print(f"     相似度: {item['similarity_score']:.3f}")
        
        # 測試 4: 相似電影
        print("\n\n" + "=" * 80)
        print("🎞️ 測試 4: 相似電影推薦 (get_similar_movies)")
        print("-" * 80)
        
        # 先找一部電影
        test_movie = movie_repo.get_all(skip=0, limit=1)[0]
        
        print(f"\n基於電影: {test_movie.title}")
        print(f"電影類型: {', '.join([mg.genre.name for mg in test_movie.genres])}")
        
        result = ai_service.get_similar_movies(
            movie_id=test_movie.id,
            top_k=5
        )
        
        if result['source_movie']:
            print(f"\n找到 {result['total']} 部相似電影:")
            for i, item in enumerate(result['similar_movies'], 1):
                print(f"\n  {i}. {item['title']}")
                print(f"     類型: {', '.join(item['genres'])}")
                print(f"     相似度: {item['similarity_score']:.3f}")
        
        print("\n\n" + "=" * 80)
        print("✅ All AI Service tests completed successfully!")
        print("=" * 80)
        
    finally:
        db.close()


if __name__ == '__main__':
    test_ai_service()
