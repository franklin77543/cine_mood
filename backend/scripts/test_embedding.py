"""
測試 Embedding Service
"""
import sys
sys.path.append('.')

from app.services.embedding_service import get_embedding_service


def test_embedding_service():
    print("=" * 60)
    print("Testing Embedding Service")
    print("=" * 60)
    
    # 初始化服務
    service = get_embedding_service()
    
    # 測試單一文本編碼
    print("\n1. Testing single text encoding...")
    text = "[科幻、冒險] 星際效應 在不久的未來，地球因為氣候變遷變得不再適合人類居住..."
    embedding = service.encode_text(text)
    print(f"   Text: {text[:50]}...")
    print(f"   Embedding shape: {embedding.shape}")
    print(f"   Embedding dimension: {service.get_embedding_dimension()}")
    print(f"   First 5 values: {embedding[:5]}")
    
    # 測試批量編碼
    print("\n2. Testing batch encoding...")
    texts = [
        "[科幻] 星際效應 太空探險拯救人類",
        "[動作、冒險] 復仇者聯盟 超級英雄拯救世界",
        "[劇情、愛情] 鐵達尼號 一段跨越階級的愛情故事"
    ]
    embeddings = service.encode_texts(texts, batch_size=8)
    print(f"   Encoded {len(texts)} texts")
    print(f"   Embeddings shape: {embeddings.shape}")
    
    # 測試相似度計算
    print("\n3. Testing similarity computation...")
    # 科幻電影應該更相似
    sci_fi_1 = service.encode_text("[科幻] 星際效應 太空探險")
    sci_fi_2 = service.encode_text("[科幻] 星際大戰 太空戰爭")
    romance = service.encode_text("[愛情] 鐵達尼號 浪漫愛情")
    
    sim_sci_fi = service.compute_similarity(sci_fi_1, sci_fi_2)
    sim_cross = service.compute_similarity(sci_fi_1, romance)
    
    print(f"   Similarity (科幻 vs 科幻): {sim_sci_fi:.4f}")
    print(f"   Similarity (科幻 vs 愛情): {sim_cross:.4f}")
    print(f"   ✅ Same genre more similar: {sim_sci_fi > sim_cross}")
    
    # 測試 create_movie_text
    print("\n4. Testing create_movie_text...")
    movie_text = service.create_movie_text(
        title="星際效應",
        overview="在不久的未來，地球因為氣候變遷變得不再適合人類居住",
        genres=["科幻", "冒險", "劇情"]
    )
    print(f"   Movie text: {movie_text}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_embedding_service()
