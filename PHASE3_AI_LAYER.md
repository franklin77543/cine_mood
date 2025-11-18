# Phase 3 - AI 智能推薦層

## 📋 目標
實現基於 AI 的電影推薦引擎，支援自然語言查詢和語意搜尋。

## 🏗️ 技術架構

```
┌──────────────────────────────────────────────────────────┐
│                    Phase 3 - AI Layer                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐   ┌────────────┐   │
│  │   Ollama     │    │  Sentence    │   │  ChromaDB  │   │
│  │ Llama3.1:8b  │───>│ Transformers │──>│  (Vectors) │   │
│  │   (NLU)      │    │  (Embedding) │   │  Storage   │   │
│  └──────────────┘    └──────────────┘   └────────────┘   │
│         │                     │                 │        │
│         ▼                     ▼                 ▼        │
│  ┌────────────────────────────────────────────────────┐  │
│  │         AI Service Layer (ai_service.py)           │  │
│  │  - parse_user_query()  - generate_embeddings()     │  │
│  │  - semantic_search()   - get_recommendations()     │  │
│  └────────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐  │
│  │      AI API Endpoints (ai_api.py)                  │  │
│  │  POST /ai/recommend - 自然語言推薦                  │  │
│  │  POST /ai/search    - 語意搜尋                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 🔧 技術棧

### AI/ML 框架
- **Ollama**: 本地 LLM 運行環境
- **Llama3.1:8b**: 語言理解模型 (自然語言意圖解析)
- **Sentence Transformers**: 文本向量化
- **ChromaDB**: 向量資料庫 (語意搜尋)

### 模型選擇
- **Embedding Model**: `paraphrase-multilingual-mpnet-base-v2`
  - 支援中文和多語言
  - 768 維向量
  - 適合語意相似度計算

## 📝 任務分解

### **Task 3.1: 環境準備**
**目標**: 安裝並測試 AI 相關依賴

**步驟**:
1. 安裝 Ollama
   - 下載: https://ollama.ai/download
   - 安裝到本機
   - 驗證: `ollama --version`

2. 下載 Llama3.1:8b 模型
   ```bash
   ollama pull llama3.1:8b
   ```

3. 測試 Ollama 連接
   ```bash
   ollama run llama3.1:8b "Hello, how are you?"
   ```

4. 安裝 Python 依賴
   ```bash
   pip install sentence-transformers chromadb ollama
   ```

5. 測試依賴
   ```python
   from sentence_transformers import SentenceTransformer
   from chromadb import Client
   import ollama
   ```

**完成標準**:
- ✅ Ollama 成功安裝並運行
- ✅ Llama3.1:8b 模型下載完成
- ✅ Python 套件安裝成功
- ✅ 所有 import 正常

---

### **Task 3.2: 向量化處理**
**目標**: 建立文本向量化服務

**檔案**: `backend/app/services/embedding_service.py`

**功能**:
```python
class EmbeddingService:
    def __init__(self):
        # 使用多語言模型
        self.model = SentenceTransformer(
            'paraphrase-multilingual-mpnet-base-v2'
        )
    
    def generate_movie_embedding(self, movie):
        """
        為電影生成向量
        組合: title + overview + genres
        """
        pass
    
    def generate_query_embedding(self, text):
        """
        為查詢文本生成向量
        """
        pass
    
    def batch_generate_embeddings(self, movies):
        """
        批次生成向量 (效能優化)
        """
        pass
```

**向量同步腳本**: `backend/scripts/sync_embeddings.py`
- 讀取所有 212 部電影
- 生成 embeddings (768 維向量)
- 儲存到 `movie_embeddings` 表
- 同時儲存到 ChromaDB

**完成標準**:
- ✅ EmbeddingService 實作完成
- ✅ 212 部電影全部向量化
- ✅ `movie_embeddings` 表資料完整
- ✅ 向量維度正確 (768)

---

### **Task 3.3: ChromaDB 整合**
**目標**: 建立向量儲存和檢索服務

**檔案**: `backend/app/services/vector_store.py`

**功能**:
```python
class VectorStore:
    def __init__(self):
        # Persistent mode
        self.client = chromadb.PersistentClient(
            path="./chroma_data"
        )
        self.collection = self.client.get_or_create_collection(
            name="cinemood_movies",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_movie(self, movie_id, embedding, metadata):
        """
        添加電影向量到 collection
        metadata: title, genres, overview, etc.
        """
        pass
    
    def search_similar(self, query_embedding, top_k=10, filters=None):
        """
        語意搜尋
        支援 metadata 篩選 (genre, year, rating)
        """
        pass
    
    def get_movie_by_id(self, movie_id):
        """
        根據 ID 獲取向量
        """
        pass
```

**ChromaDB 配置**:
- Collection name: `cinemood_movies`
- Distance metric: Cosine similarity
- Persistent storage: `backend/chroma_data/`

**完成標準**:
- ✅ VectorStore 實作完成
- ✅ ChromaDB collection 建立成功
- ✅ 所有電影向量已儲存
- ✅ 語意搜尋測試通過

---

### **Task 3.4: Ollama NLU 整合**
**目標**: 使用 LLM 解析使用者意圖

**檔案**: `backend/app/services/llm_service.py`

**功能**:
```python
class LLMService:
    def __init__(self):
        self.model = "llama3.1:8b"
        self.base_url = "http://localhost:11434"
    
    def parse_user_intent(self, query):
        """
        解析使用者查詢意圖
        
        輸入: "我想看輕鬆搞笑的電影"
        輸出: {
            "mood": "輕鬆",
            "genres": ["喜劇"],
            "keywords": ["搞笑"],
            "preferences": {}
        }
        """
        pass
    
    def generate_recommendation_reason(self, movie, user_query):
        """
        生成推薦理由
        
        為什麼推薦這部電影給使用者
        """
        pass
    
    def extract_keywords(self, text):
        """
        提取關鍵字
        """
        pass
```

**Prompt Engineering**:
```python
INTENT_PARSE_PROMPT = """
你是一個電影推薦助手。請分析使用者的查詢，提取以下資訊：

1. 心情/情緒 (mood)
2. 電影類型 (genres)
3. 關鍵字 (keywords)
4. 其他偏好 (preferences)

查詢: {user_query}

請以 JSON 格式回答。
"""

RECOMMENDATION_REASON_PROMPT = """
根據使用者的查詢和電影資訊，生成推薦理由。

使用者查詢: {user_query}
電影標題: {movie_title}
電影簡介: {movie_overview}
電影類型: {movie_genres}

請用 1-2 句話說明為什麼推薦這部電影。
"""
```

**完成標準**:
- ✅ LLMService 實作完成
- ✅ Ollama 連接成功
- ✅ 意圖解析準確度 > 80%
- ✅ 推薦理由生成合理
- ✅ 支援中文查詢

---

### **Task 3.5: AI 推薦服務**
**目標**: 整合 LLM + Embedding + Vector Search

**檔案**: `backend/app/services/ai_service.py`

**功能**:
```python
class AIService:
    def __init__(self, db):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
    
    def get_recommendations(self, user_query, top_k=10):
        """
        主要推薦流程:
        
        1. LLM 解析查詢意圖
        2. 生成查詢 embedding
        3. ChromaDB 語意搜尋
        4. 結合 metadata 篩選 (genre, mood)
        5. LLM 生成推薦理由
        6. 返回結果
        
        返回: [
            {
                "movie": MovieDetail,
                "similarity_score": 0.85,
                "reason": "這部電影..."
            }
        ]
        """
        pass
    
    def semantic_search(self, query, filters=None, top_k=10):
        """
        純向量搜尋 (不經過 LLM)
        
        適合簡單語意搜尋
        """
        pass
    
    def get_similar_movies(self, movie_id, top_k=10):
        """
        根據電影找相似電影
        """
        pass
```

**推薦演算法**:
```python
def hybrid_search(user_query):
    # 1. LLM 意圖解析
    intent = llm_service.parse_user_intent(user_query)
    
    # 2. 生成查詢向量
    query_embedding = embedding_service.generate_query_embedding(
        user_query
    )
    
    # 3. 向量搜尋 (top 20)
    vector_results = vector_store.search_similar(
        query_embedding, 
        top_k=20
    )
    
    # 4. Metadata 篩選
    if intent.get('genres'):
        results = filter_by_genres(vector_results, intent['genres'])
    
    # 5. 重新排序 (相似度 + metadata 匹配度)
    ranked_results = rerank(results, intent)
    
    # 6. 生成推薦理由
    for result in ranked_results[:10]:
        result['reason'] = llm_service.generate_recommendation_reason(
            result['movie'], user_query
        )
    
    return ranked_results[:10]
```

**完成標準**:
- ✅ AIService 實作完成
- ✅ 推薦流程測試通過
- ✅ 混合檢索正常運作
- ✅ 推薦理由生成合理

---

### **Task 3.6: AI API 端點**
**目標**: 暴露 AI 推薦功能為 REST API

**檔案**: `backend/app/api/ai_api.py`

**端點 1: 智能推薦**
```python
@router.post("/recommend", response_model=RecommendationResponse)
def get_ai_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/ai/recommend
    
    Request:
    {
        "query": "我想看輕鬆搞笑的電影",
        "top_k": 10
    }
    
    Response:
    {
        "query": "我想看輕鬆搞笑的電影",
        "intent": {
            "mood": "輕鬆",
            "genres": ["喜劇"],
            "keywords": ["搞笑"]
        },
        "recommendations": [
            {
                "movie": MovieDetail,
                "similarity_score": 0.85,
                "reason": "這是一部輕鬆搞笑的喜劇片..."
            }
        ],
        "total": 10
    }
    """
    pass
```

**端點 2: 語意搜尋**
```python
@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(
    request: SemanticSearchRequest,
    db: Session = Depends(get_db)
):
    """
    POST /api/v1/ai/search
    
    Request:
    {
        "query": "太空探險",
        "top_k": 5,
        "filters": {
            "genres": ["科幻"],
            "min_rating": 7.0
        }
    }
    
    Response:
    {
        "query": "太空探險",
        "results": [
            {
                "movie": MovieDetail,
                "similarity_score": 0.92
            }
        ],
        "total": 5
    }
    """
    pass
```

**端點 3: 相似電影**
```python
@router.get("/similar/{movie_id}", response_model=SimilarMoviesResponse)
def get_similar_movies(
    movie_id: str,
    top_k: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    GET /api/v1/ai/similar/{movie_id}?top_k=10
    
    根據電影 ID 找相似電影
    """
    pass
```

**Pydantic Schemas**:
```python
# backend/app/schemas/ai_schema.py

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 10

class UserIntent(BaseModel):
    mood: Optional[str] = None
    genres: List[str] = []
    keywords: List[str] = []
    preferences: dict = {}

class RecommendationItem(BaseModel):
    movie: MovieDetail
    similarity_score: float
    reason: str

class RecommendationResponse(BaseModel):
    query: str
    intent: UserIntent
    recommendations: List[RecommendationItem]
    total: int
```

**註冊路由**: 更新 `backend/app/main.py`
```python
from app.api import ai_api

app.include_router(ai_api.router, prefix=settings.API_V1_PREFIX)
```

**完成標準**:
- ✅ 3 個 API 端點實作完成
- ✅ Pydantic schemas 定義完整
- ✅ 路由註冊成功
- ✅ Swagger UI 顯示正確

---

### **Task 3.7: 測試與優化**
**目標**: 全面測試 AI 功能並優化

**測試腳本**: `backend/scripts/test_ai.py`

**測試案例**:
```python
def test_mood_query():
    """測試心情查詢"""
    response = requests.post(
        "http://localhost:8000/api/v1/ai/recommend",
        json={"query": "我心情不好，想看療癒的電影"}
    )
    assert response.status_code == 200
    # 驗證推薦結果包含療癒類型電影

def test_genre_query():
    """測試類型查詢"""
    response = requests.post(
        "http://localhost:8000/api/v1/ai/recommend",
        json={"query": "推薦科幻動作片"}
    )
    # 驗證結果包含科幻和動作類型

def test_plot_query():
    """測試劇情查詢"""
    response = requests.post(
        "http://localhost:8000/api/v1/ai/recommend",
        json={"query": "有關時間旅行的故事"}
    )
    # 驗證語意搜尋找到相關電影

def test_mixed_query():
    """測試混合查詢"""
    response = requests.post(
        "http://localhost:8000/api/v1/ai/recommend",
        json={"query": "輕鬆搞笑但有深度的家庭電影"}
    )
    # 驗證多條件推薦

def test_semantic_search():
    """測試語意搜尋"""
    response = requests.post(
        "http://localhost:8000/api/v1/ai/search",
        json={
            "query": "太空探險",
            "filters": {"genres": ["科幻"]}
        }
    )
    # 驗證語意相似度

def test_similar_movies():
    """測試相似電影"""
    movie_id = "a363f3c8-a3c2-46ea-8416-ce1670864de4"
    response = requests.get(
        f"http://localhost:8000/api/v1/ai/similar/{movie_id}"
    )
    # 驗證相似電影推薦
```

**效能評估**:
```python
def evaluate_recommendations():
    """評估推薦準確度"""
    test_queries = [
        "我想看輕鬆搞笑的電影",
        "推薦科幻動作片",
        "有關時間旅行的故事",
        # ... 更多測試查詢
    ]
    
    for query in test_queries:
        results = get_recommendations(query)
        # 計算準確度指標
        # - 相關度分數
        # - 類型匹配率
        # - 推薦理由合理性
```

**優化項目**:
1. **Embedding 優化**
   - 調整文本組合策略 (title vs overview 權重)
   - 嘗試不同的 embedding 模型

2. **ChromaDB 優化**
   - 調整相似度閾值
   - 優化檢索參數 (top_k, distance)

3. **LLM Prompt 優化**
   - 改進意圖解析提示詞
   - 優化推薦理由生成

4. **效能優化**
   - Embedding 快取
   - 批次處理
   - 非同步呼叫

**完成標準**:
- ✅ 所有測試案例通過
- ✅ 推薦準確度 > 70%
- ✅ 回應時間 < 3 秒
- ✅ 推薦理由合理且中文流暢

---

## 🎯 完成標準總覽

### 1. 環境與依賴
- ✅ Ollama 成功安裝並運行
- ✅ Llama3.1:8b 模型下載完成
- ✅ Python 依賴安裝成功
- ✅ ChromaDB 初始化成功

### 2. 向量化
- ✅ 212 部電影全部向量化
- ✅ `movie_embeddings` 表資料完整
- ✅ ChromaDB collection 包含所有向量
- ✅ 向量維度正確 (768)

### 3. 語意搜尋
- ✅ 中文查詢能找到相關電影
- ✅ Top 10 結果相關度 > 70%
- ✅ 支援 metadata 篩選

### 4. NLU 解析
- ✅ 能識別心情、類型、劇情關鍵字
- ✅ 支援中文自然語言
- ✅ 意圖解析準確度 > 80%

### 5. API 端點
- ✅ `/ai/recommend` 返回推薦 + 理由
- ✅ `/ai/search` 返回語意相似結果
- ✅ `/ai/similar/{id}` 返回相似電影
- ✅ 錯誤處理完善
- ✅ Swagger UI 文檔完整

### 6. 測試與優化
- ✅ 4 種查詢類型測試通過
- ✅ 推薦準確度達標
- ✅ 回應時間 < 3 秒
- ✅ 推薦理由合理

---

## 🔧 技術亮點

### 1. 多語言支援
- 使用 `paraphrase-multilingual-mpnet-base-v2` embedding 模型
- 支援中文、英文混合查詢
- 中文電影資料完整支援

### 2. 混合檢索
- 向量語意搜尋 (Embedding + ChromaDB)
- Metadata 篩選 (類型、評分、年份)
- LLM 意圖增強
- 多維度排序演算法

### 3. 本地部署
- 所有 AI 模型在本機運行
- 無需外部 API 調用
- 資料隱私保護
- 成本可控

### 4. 效能優化
- ChromaDB persistent mode
- Embedding 批次生成
- 向量快取機制
- 非同步處理

### 5. 智能推薦
- LLM 驅動的意圖理解
- 自動生成推薦理由
- 上下文感知推薦
- 個性化結果排序

---

## ⏱️ 開發時程

| 任務 | 預估時間 | 實際時間 |
|------|----------|----------|
| Task 3.1: 環境準備 | 30 min | - |
| Task 3.2: 向量化處理 | 1 hr | - |
| Task 3.3: ChromaDB 整合 | 1 hr | - |
| Task 3.4: Ollama NLU 整合 | 1.5 hr | - |
| Task 3.5: AI 推薦服務 | 1.5 hr | - |
| Task 3.6: AI API 端點 | 1 hr | - |
| Task 3.7: 測試與優化 | 1.5 hr | - |
| **總計** | **8 小時** | **-** |

**實際可能**: 4-6 小時 (視硬體效能和除錯時間)

---

## 📚 參考資源

### Ollama
- 官網: https://ollama.ai/
- 文檔: https://github.com/ollama/ollama/blob/main/docs/api.md
- Llama 3.1 模型: https://ollama.ai/library/llama3.1

### Sentence Transformers
- 文檔: https://www.sbert.net/
- 多語言模型: https://www.sbert.net/docs/pretrained_models.html
- 中文支援: `paraphrase-multilingual-mpnet-base-v2`

### ChromaDB
- 文檔: https://docs.trychroma.com/
- Python Client: https://docs.trychroma.com/reference/py-client
- Getting Started: https://docs.trychroma.com/getting-started

### Prompt Engineering
- OpenAI Best Practices: https://platform.openai.com/docs/guides/prompt-engineering
- LangChain Prompts: https://python.langchain.com/docs/modules/model_io/prompts/

---

## 🚀 下一步

完成 Phase 3 後，進入 **Phase 4 - 前端開發**:
- React.js + TypeScript 前端
- Zustand 狀態管理
- Tailwind CSS 樣式
- 整合 Phase 2 API 和 Phase 3 AI 推薦

**準備好開始 Phase 3 了嗎？** 🎬
