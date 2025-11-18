"""
Vector Store
自定義向量存儲系統（替代 ChromaDB）
使用 numpy 實現基於餘弦相似度的向量搜尋
"""
import numpy as np
import pickle
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """向量存儲和檢索系統"""
    
    def __init__(self, embedding_dim: int = 768):
        """
        初始化向量存儲
        
        Args:
            embedding_dim: 向量維度
        """
        self.embedding_dim = embedding_dim
        self.vectors = np.array([]).reshape(0, embedding_dim)  # (n_vectors, dim)
        self.metadata = []  # List of dicts containing movie info
        self.movie_id_to_index = {}  # movie_id -> vector index mapping
    
    def add(self, movie_id: str, vector: np.ndarray, metadata: Dict):
        """
        添加向量到存儲
        
        Args:
            movie_id: 電影 ID
            vector: 向量 (768,)
            metadata: 電影元資料 (title, overview, genres, etc.)
        """
        if movie_id in self.movie_id_to_index:
            # 更新現有向量
            index = self.movie_id_to_index[movie_id]
            self.vectors[index] = vector
            self.metadata[index] = metadata
        else:
            # 添加新向量
            self.vectors = np.vstack([self.vectors, vector.reshape(1, -1)])
            self.metadata.append(metadata)
            self.movie_id_to_index[movie_id] = len(self.metadata) - 1
    
    def add_batch(self, movie_ids: List[str], vectors: np.ndarray, metadata_list: List[Dict]):
        """
        批量添加向量
        
        Args:
            movie_ids: 電影 ID 列表
            vectors: 向量矩陣 (n, 768)
            metadata_list: 元資料列表
        """
        for movie_id, vector, metadata in zip(movie_ids, vectors, metadata_list):
            self.add(movie_id, vector, metadata)
    
    def search(
        self, 
        query_vector: np.ndarray, 
        top_k: int = 10,
        filter_genre: Optional[str] = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        搜尋最相似的向量
        
        Args:
            query_vector: 查詢向量 (768,)
            top_k: 返回前 k 個結果
            filter_genre: 可選的類型篩選
            
        Returns:
            List of (movie_id, similarity, metadata)
        """
        if len(self.vectors) == 0:
            return []
        
        # 計算餘弦相似度
        # 正規化查詢向量
        query_norm = query_vector / (np.linalg.norm(query_vector) + 1e-10)
        
        # 正規化所有向量
        vectors_norm = self.vectors / (np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-10)
        
        # 計算相似度
        similarities = np.dot(vectors_norm, query_norm)
        
        # 類型篩選
        if filter_genre:
            valid_indices = []
            for idx, metadata in enumerate(self.metadata):
                genres = metadata.get('genres', [])
                if filter_genre in genres:
                    valid_indices.append(idx)
            
            if not valid_indices:
                return []
            
            # 只保留符合類型的結果
            filtered_similarities = [(idx, similarities[idx]) for idx in valid_indices]
            filtered_similarities.sort(key=lambda x: x[1], reverse=True)
            top_indices = [idx for idx, _ in filtered_similarities[:top_k]]
            top_similarities = [sim for _, sim in filtered_similarities[:top_k]]
        else:
            # 獲取 top-k
            top_indices = np.argsort(similarities)[::-1][:top_k]
            top_similarities = similarities[top_indices]
        
        # 準備結果
        results = []
        for idx, sim in zip(top_indices, top_similarities):
            movie_id = self.metadata[idx]['movie_id']
            metadata = self.metadata[idx]
            results.append((movie_id, float(sim), metadata))
        
        return results
    
    def get_by_movie_id(self, movie_id: str) -> Optional[Tuple[np.ndarray, Dict]]:
        """根據 movie_id 獲取向量和元資料"""
        if movie_id not in self.movie_id_to_index:
            return None
        
        index = self.movie_id_to_index[movie_id]
        return self.vectors[index], self.metadata[index]
    
    def save(self, filepath: str):
        """保存向量存儲到檔案"""
        data = {
            'embedding_dim': self.embedding_dim,
            'vectors': self.vectors,
            'metadata': self.metadata,
            'movie_id_to_index': self.movie_id_to_index
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Vector store saved to {filepath} ({len(self.metadata)} vectors)")
    
    def load(self, filepath: str):
        """從檔案載入向量存儲"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.embedding_dim = data['embedding_dim']
        self.vectors = data['vectors']
        self.metadata = data['metadata']
        self.movie_id_to_index = data['movie_id_to_index']
        
        logger.info(f"Vector store loaded from {filepath} ({len(self.metadata)} vectors)")
    
    def __len__(self):
        """返回存儲的向量數量"""
        return len(self.metadata)
    
    def get_stats(self) -> Dict:
        """獲取統計資訊"""
        return {
            'total_vectors': len(self.metadata),
            'embedding_dim': self.embedding_dim,
            'memory_size_mb': self.vectors.nbytes / (1024 * 1024)
        }


# 全域單例
_vector_store = None


def get_vector_store() -> VectorStore:
    """獲取 Vector Store 單例"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
