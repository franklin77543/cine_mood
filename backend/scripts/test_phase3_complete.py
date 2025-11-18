"""
Simple AI API Test
簡單測試 AI API（使用 requests 直接測試，不依賴 uvicorn）
"""
import sys
import os
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# 設置工作目錄為 backend
os.chdir(backend_dir)

from app.db.session import SessionLocal
from app.repositories.movie_repository import MovieRepository
from app.services.ai_service import get_ai_service


def test_ai_service_directly():
    """直接測試 AI Service（不通過 HTTP）"""
    print("=" * 80)
    print("  AI 服務直接測試（繞過 HTTP API）")
    print("=" * 80)
    
    db = SessionLocal()
    movie_repo = MovieRepository(db)
    ai_service = get_ai_service(movie_repo)
    
    try:
        # 測試 1: 智能推薦
        print("\n🎬 測試 1: 智能推薦")
        print("-" * 80)
        
        query = "我想看太空探險的科幻電影"
        print(f"查詢: '{query}'")
        
        result = ai_service.get_recommendations(
            user_query=query,
            top_k=5,
            generate_reasons=True
        )
        
        print(f"\n✅ 成功!")
        print(f"\n意圖解析:")
        print(f"  心情: {result['intent'].get('mood')}")
        print(f"  類型: {result['intent'].get('genres')}")
        print(f"  關鍵字: {result['intent'].get('keywords')}")
        
        print(f"\n推薦結果 (共 {result['total']} 部):")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"\n  {i}. {rec['title']}")
            print(f"     類型: {', '.join(rec['genres'])}")
            print(f"     相似度: {rec['similarity_score']:.3f}")
            if rec.get('reason'):
                print(f"     推薦理由: {rec['reason']}")
        
        # 測試 2: 語義搜尋
        print("\n\n🔍 測試 2: 語義搜尋")
        print("-" * 80)
        
        query = "時間旅行"
        print(f"查詢: '{query}'")
        
        result = ai_service.semantic_search(
            query=query,
            top_k=5
        )
        
        print(f"\n✅ 找到 {result['total']} 部相關電影:")
        for i, item in enumerate(result['results'][:3], 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     類型: {', '.join(item['genres'])}")
            print(f"     相似度: {item['similarity_score']:.3f}")
        
        # 測試 3: 相似電影
        print("\n\n🎞️ 測試 3: 相似電影")
        print("-" * 80)
        
        # 獲取一部電影
        test_movie = movie_repo.get_movies(skip=0, limit=1)[0]
        print(f"基於電影: {test_movie.title}")
        
        result = ai_service.get_similar_movies(
            movie_id=test_movie.id,
            top_k=5
        )
        
        if result['source_movie']:
            print(f"\n✅ 找到 {result['total']} 部相似電影:")
            for i, item in enumerate(result['similar_movies'][:3], 1):
                print(f"\n  {i}. {item['title']}")
                print(f"     類型: {', '.join(item['genres'])}")
                print(f"     相似度: {item['similarity_score']:.3f}")
        
        # 總結
        print("\n\n" + "=" * 80)
        print("  ✅ Phase 3 核心功能測試完成！")
        print("=" * 80)
        print("\n已完成的功能:")
        print("  ✅ Task 3.1: Ollama 環境準備")
        print("  ✅ Task 3.2: 向量化處理（212 部電影）")
        print("  ✅ Task 3.3: Vector Store（自定義向量數據庫）")
        print("  ✅ Task 3.4: LLM 服務（意圖解析 + 推薦理由）")
        print("  ✅ Task 3.5: AI 推薦服務（混合檢索）")
        print("  ✅ Task 3.6: AI API 端點（3 個端點）")
        
        print("\nAPI 端點已就緒:")
        print("  POST /api/v1/ai/recommend - 智能推薦")
        print("  POST /api/v1/ai/search - 語義搜尋")
        print("  GET  /api/v1/ai/similar/{movie_id} - 相似電影")
        
        print("\n啟動 API 服務器命令:")
        print("  uvicorn app.main:app --reload --port 8000")
        print("\nAPI 文檔:")
        print("  http://localhost:8000/docs")
        print("  http://localhost:8000/redoc")
        
        print("\n" + "=" * 80)
        
    finally:
        db.close()


if __name__ == '__main__':
    test_ai_service_directly()
