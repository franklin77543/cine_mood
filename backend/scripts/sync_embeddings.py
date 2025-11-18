"""
Sync Embeddings
為所有電影生成向量嵌入並存儲
"""
import sys
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.movie_model import Movie
from app.services.embedding_service import get_embedding_service
from app.services.vector_store import get_vector_store
from tqdm import tqdm


def sync_embeddings():
    """同步所有電影的向量嵌入"""
    print("Starting embedding sync...")
    
    # 初始化服務
    db = SessionLocal()
    embedding_service = get_embedding_service()
    vector_store = get_vector_store()
    
    try:
        # 獲取所有電影
        movies = db.query(Movie).all()
        print(f"Found {len(movies)} movies in database")
        
        # 批量處理
        batch_size = 32
        for i in tqdm(range(0, len(movies), batch_size), desc="Generating embeddings"):
            batch_movies = movies[i:i + batch_size]
            
            # 準備文本
            movie_ids = []
            texts = []
            metadata_list = []
            
            for movie in batch_movies:
                # 獲取類型名稱（通過 MovieGenre 關聯到 Genre）
                genre_names = [mg.genre.name for mg in movie.genres]
                
                # 創建電影文本
                text = embedding_service.create_movie_text(
                    title=movie.title,
                    overview=movie.overview or "",
                    genres=genre_names
                )
                
                # 準備元資料
                metadata = {
                    'movie_id': str(movie.id),
                    'title': movie.title,
                    'overview': movie.overview,
                    'genres': genre_names,
                    'release_date': str(movie.release_date) if movie.release_date else None,
                    'poster_path': movie.poster_path,
                    'backdrop_path': movie.backdrop_path,
                    'vote_average': movie.vote_average,
                    'popularity': movie.popularity
                }
                
                movie_ids.append(str(movie.id))
                texts.append(text)
                metadata_list.append(metadata)
            
            # 生成向量
            embeddings = embedding_service.encode_texts(texts)
            
            # 添加到向量存儲
            vector_store.add_batch(movie_ids, embeddings, metadata_list)
        
        # 保存向量存儲
        store_path = backend_dir / 'data' / 'vector_store.pkl'
        vector_store.save(str(store_path))
        
        # 顯示統計
        stats = vector_store.get_stats()
        print(f"\n✅ Embedding sync completed!")
        print(f"   Total vectors: {stats['total_vectors']}")
        print(f"   Embedding dimension: {stats['embedding_dim']}")
        print(f"   Memory size: {stats['memory_size_mb']:.2f} MB")
        print(f"   Saved to: {store_path}")
        
    finally:
        db.close()


if __name__ == '__main__':
    sync_embeddings()
