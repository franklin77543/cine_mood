"""
Embedding Service
使用 Sentence Transformers 生成電影描述的向量表示
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    """向量嵌入服務"""
    
    def __init__(self, model_name: str = "paraphrase-multilingual-mpnet-base-v2"):
        """
        初始化 Embedding 模型
        
        Args:
            model_name: Hugging Face 模型名稱，預設使用支援中文的多語言模型
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """載入 Sentence Transformer 模型"""
        print(f"Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        print(f"✅ Model loaded successfully!")
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        將單一文本編碼為向量
        
        Args:
            text: 要編碼的文本
            
        Returns:
            向量表示 (768 維)
        """
        if not text or len(text.strip()) == 0:
            # 返回零向量
            return np.zeros(768)
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def encode_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        批量編碼多個文本
        
        Args:
            texts: 文本列表
            batch_size: 批次大小
            
        Returns:
            向量矩陣 (n_texts, 768)
        """
        embeddings = self.model.encode(
            texts, 
            convert_to_numpy=True,
            batch_size=batch_size,
            show_progress_bar=True
        )
        return embeddings
    
    def create_movie_text(self, title: str, overview: str, genres: List[str]) -> str:
        """
        組合電影資訊為單一文本用於 embedding
        
        Args:
            title: 電影標題
            overview: 電影簡介
            genres: 類型列表
            
        Returns:
            組合後的文本
        """
        # 組合格式：[類型] 標題。簡介
        genre_text = "、".join(genres) if genres else ""
        
        parts = []
        if genre_text:
            parts.append(f"[{genre_text}]")
        if title:
            parts.append(title)
        if overview:
            parts.append(overview)
        
        return " ".join(parts)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        計算兩個向量的餘弦相似度
        
        Args:
            embedding1: 第一個向量
            embedding2: 第二個向量
            
        Returns:
            相似度分數 (0-1)
        """
        # 餘弦相似度
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        # 將 -1~1 映射到 0~1
        return (similarity + 1) / 2
    
    def get_embedding_dimension(self) -> int:
        """獲取 embedding 維度"""
        return self.model.get_sentence_embedding_dimension()


# 全域單例
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """獲取 Embedding Service 單例"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
