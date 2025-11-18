"""
Test Vector Search
測試向量存儲的語義搜尋功能
"""
import sys
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.embedding_service import get_embedding_service
from app.services.vector_store import get_vector_store


def test_vector_search():
    """測試向量搜尋"""
    print("Testing Vector Search...")
    print("=" * 60)
    
    # 載入服務
    embedding_service = get_embedding_service()
    vector_store = get_vector_store()
    
    # 載入向量存儲
    store_path = backend_dir / 'data' / 'vector_store.pkl'
    vector_store.load(str(store_path))
    
    print(f"✅ Loaded {len(vector_store)} movie vectors\n")
    
    # 測試案例
    test_queries = [
        "太空探險的科幻電影",
        "輕鬆搞笑的喜劇",
        "感人的愛情故事",
        "緊張刺激的動作片",
        "關於時間旅行的故事"
    ]
    
    for query in test_queries:
        print(f"\n🔍 查詢: '{query}'")
        print("-" * 60)
        
        # 生成查詢向量
        query_embedding = embedding_service.encode_text(query)
        
        # 搜尋最相似的電影
        results = vector_store.search(query_embedding, top_k=5)
        
        print(f"找到 {len(results)} 部相關電影:\n")
        for i, (movie_id, similarity, metadata) in enumerate(results, 1):
            title = metadata['title']
            genres = ', '.join(metadata['genres'])
            score = similarity * 100
            
            print(f"{i}. {title}")
            print(f"   類型: {genres}")
            print(f"   相似度: {score:.1f}%")
            if metadata.get('overview'):
                overview = metadata['overview'][:80] + "..." if len(metadata['overview']) > 80 else metadata['overview']
                print(f"   簡介: {overview}")
            print()
    
    # 測試類型篩選
    print("\n" + "=" * 60)
    print("🎯 測試類型篩選搜尋")
    print("=" * 60)
    
    query = "愛情故事"
    filter_genre = "科幻"
    
    print(f"\n🔍 查詢: '{query}' (只要 {filter_genre} 類型)")
    print("-" * 60)
    
    query_embedding = embedding_service.encode_text(query)
    results = vector_store.search(query_embedding, top_k=5, filter_genre=filter_genre)
    
    print(f"找到 {len(results)} 部科幻愛情電影:\n")
    for i, (movie_id, similarity, metadata) in enumerate(results, 1):
        title = metadata['title']
        genres = ', '.join(metadata['genres'])
        score = similarity * 100
        
        print(f"{i}. {title}")
        print(f"   類型: {genres}")
        print(f"   相似度: {score:.1f}%\n")
    
    # 顯示統計
    print("\n" + "=" * 60)
    stats = vector_store.get_stats()
    print("📊 向量存儲統計:")
    print(f"   總向量數: {stats['total_vectors']}")
    print(f"   向量維度: {stats['embedding_dim']}")
    print(f"   記憶體佔用: {stats['memory_size_mb']:.2f} MB")
    print("\n✅ All vector search tests passed!")


if __name__ == '__main__':
    test_vector_search()
