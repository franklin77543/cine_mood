"""
Test LLM Service
測試 Ollama LLM 意圖解析和推薦理由生成
"""
import sys
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.llm_service import get_llm_service


def test_llm_service():
    """測試 LLM 服務"""
    print("Testing LLM Service with Ollama...")
    print("=" * 60)
    
    llm_service = get_llm_service()
    
    # 測試意圖解析
    print("\n📝 測試 1: 意圖解析")
    print("-" * 60)
    
    test_queries = [
        "我想看輕鬆搞笑的電影",
        "推薦科幻動作片",
        "有關時間旅行的故事",
        "心情不好，想看療癒的電影",
        "緊張刺激的懸疑片"
    ]
    
    for query in test_queries:
        print(f"\n查詢: '{query}'")
        intent = llm_service.parse_user_intent(query)
        print(f"解析結果:")
        print(f"  心情: {intent.get('mood')}")
        print(f"  類型: {intent.get('genres')}")
        print(f"  關鍵字: {intent.get('keywords')}")
        print(f"  偏好: {intent.get('preferences')}")
    
    # 測試推薦理由生成
    print("\n\n" + "=" * 60)
    print("💬 測試 2: 推薦理由生成")
    print("-" * 60)
    
    test_cases = [
        {
            "query": "我想看太空探險的科幻電影",
            "title": "星際效應",
            "genres": ["科幻", "冒險", "劇情"],
            "overview": "由於地球即將毀滅，一群探險家扛起人類史上最重要的任務：越過已知的銀河，在星際間尋找人類未來的可能性。"
        },
        {
            "query": "輕鬆搞笑的喜劇",
            "title": "回到未來",
            "genres": ["科幻", "喜劇", "冒險"],
            "overview": "米高福克斯飾演一個80年代的青少年，他在一個科學家的幫助下，通過時光隧道回到50年代。"
        },
        {
            "query": "感人的愛情故事",
            "title": "愛上觸不到的你",
            "genres": ["愛情", "劇情"],
            "overview": "17歲史黛拉和威爾同為囊狀纖維化症患者，在醫院接受治療時相愛，但為了控制病情必須保持距離。"
        }
    ]
    
    for case in test_cases:
        print(f"\n查詢: '{case['query']}'")
        print(f"電影: {case['title']} ({', '.join(case['genres'])})")
        
        reason = llm_service.generate_recommendation_reason(
            movie_title=case['title'],
            movie_overview=case['overview'],
            movie_genres=case['genres'],
            user_query=case['query']
        )
        
        print(f"推薦理由: {reason}")
    
    # 測試關鍵字提取
    print("\n\n" + "=" * 60)
    print("🔑 測試 3: 關鍵字提取")
    print("-" * 60)
    
    texts = [
        "一部關於太空探險和時間旅行的科幻電影",
        "輕鬆搞笑但有深度的家庭喜劇",
        "緊張刺激的動作冒險故事"
    ]
    
    for text in texts:
        print(f"\n文本: '{text}'")
        keywords = llm_service.extract_keywords(text)
        print(f"關鍵字: {', '.join(keywords)}")
    
    print("\n\n✅ All LLM tests completed!")


if __name__ == '__main__':
    test_llm_service()
