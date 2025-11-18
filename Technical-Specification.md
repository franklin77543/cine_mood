# CineMood 技術規格文件

## 1. 系統架構

### 1.1 System Architecture
```
┌─────────────────────────┐
│    Frontend Layer       │
│      (Web UI)           │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│      API Layer          │
│      (RESTful)          │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│   Backend Services      │
│  ┌─────────────────┐    │
│  │  NLP   │  Rec   │    │
│  │Service │Engine  │    │
│  └─────────────────┘    │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│      Data Layer         │
│  ┌─────────────────┐    │
│  │ Movie │ Cache   │    │
│  │  DB   │ Layer   │    │
│  └─────────────────┘    │
└─────────────────────────┘
```

### 1.2 技術棧選擇

#### 前端
- **框架**: React.js
- **UI 框架**: Tailwind CSS
- **狀態管理**: Zustand
- **語言**: TypeScript

#### 後端
- **框架**: Python FastAPI
- **語言**: Python 3.13+
- **API 規範**: RESTful API
- **架構模式**: 分層架構 (Repository → Service → API)

#### 資料庫
- **主資料庫**: SQLite
- **向量資料庫**: ChromaDB (本地向量搜尋)
- **快取**: 內建記憶體快取 (functools.lru_cache)

#### AI/NLP
- **LLM**: Ollama + Llama3.1:8b
- **嵌入模型**: Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **情緒分析**: Llama3.1:8b

---

## 2. 核心模組規格

### 2.1 自然語言理解模組 (NLU Module)

#### 2.1.1 功能職責
- 接收使用者輸入文字
- 分析輸入意圖（搜尋類型）
- 提取關鍵資訊（實體識別）
- 情緒分析

#### 2.1.2 輸入/輸出規格
```typescript
// 輸入
interface UserInput {
  text: string;
  userId?: string;
  sessionId?: string;
  timestamp: Date;
}

// 輸出
interface ParsedIntent {
  intentType: 'exact' | 'fuzzy' | 'mood' | 'question';
  entities: {
    movieName?: string;
    director?: string;
    actor?: string;
    genre?: string[];
    year?: number;
    keywords?: string[];
  };
  mood?: {
    emotion: string;      // e.g., 'sad', 'happy', 'stressed'
    intensity: number;    // 0-1
  };
  searchQuery: string;
  confidence: number;     // 0-1
}
```

#### 2.1.3 實作方法

**方案 A: LLM-based (推薦)**
```python
# 使用 LLM 進行意圖解析
def parse_user_input(user_input: str) -> ParsedIntent:
    prompt = f"""
    分析以下使用者輸入，提取電影搜尋意圖：
    
    使用者輸入: "{user_input}"
    
    請以 JSON 格式返回：
    1. intentType: exact/fuzzy/mood/question
    2. entities: 提取的電影名稱、演員、導演、類型等
    3. mood: 如果有情緒表達，識別情緒類型和強度
    4. searchQuery: 優化後的搜尋關鍵字
    """
    
    response = llm.complete(prompt)
    return parse_json(response)
```

**方案 B: 規則 + 機器學習混合**
- 使用正則表達式處理精確匹配
- 使用情緒詞典進行情緒分類
- 使用 NER 模型提取實體

---

### 2.2 推薦引擎模組 (Recommendation Engine)

#### 2.2.1 功能職責
- 根據解析後的意圖生成電影推薦
- 計算電影與輸入的相關度
- 排序和過濾推薦結果

#### 2.2.2 推薦策略

**策略 1: 精確搜尋**
```python
def exact_search(entities: dict) -> List[Movie]:
    # 資料庫查詢
    query = build_sql_query(entities)
    results = db.execute(query)
    return results
```

**策略 2: 語義搜尋**
```python
def semantic_search(search_query: str, top_k: int = 10) -> List[Movie]:
    # 1. 將查詢轉換為向量
    query_embedding = embedding_model.encode(search_query)
    
    # 2. 在向量資料庫中搜尋
    similar_movies = vector_db.similarity_search(
        query_embedding, 
        top_k=top_k
    )
    
    return similar_movies
```

**策略 3: 情緒映射**
```python
# 情緒與電影屬性映射表
MOOD_TO_GENRES = {
    'sad': ['drama', 'romance'],
    'happy': ['comedy', 'animation', 'musical'],
    'stressed': ['comedy', 'light-hearted'],
    'thoughtful': ['sci-fi', 'drama', 'documentary'],
    'excited': ['action', 'adventure', 'thriller']
}

def mood_based_search(mood: dict) -> List[Movie]:
    emotion = mood['emotion']
    genres = MOOD_TO_GENRES.get(emotion, [])
    
    # 查詢符合類型的高評分電影
    results = db.query(
        genres=genres,
        min_rating=7.0,
        order_by='rating DESC'
    )
    
    return results
```

#### 2.2.3 推薦結果規格
```typescript
interface MovieRecommendation {
  movie: {
    id: string;
    title: string;
    titleOriginal: string;
    posterUrl: string;
    releaseYear: number;
    genres: string[];
    director: string;
    cast: string[];
    rating: number;
    summary: string;
    runtime: number;
  };
  matchScore: number;        // 0-1
  recommendationReason: string;  // 為何推薦此片
}

interface RecommendationResponse {
  recommendations: MovieRecommendation[];
  totalCount: number;
  searchIntent: ParsedIntent;
}
```

---

### 2.3 電影資料模組

#### 2.3.1 資料庫結構

```sql
-- 電影主表
CREATE TABLE movies (
    id UUID PRIMARY KEY,
    tmdb_id INTEGER UNIQUE,
    title VARCHAR(500) NOT NULL,
    title_original VARCHAR(500),
    release_date DATE,
    runtime INTEGER,
    overview TEXT,
    poster_path VARCHAR(500),
    backdrop_path VARCHAR(500),
    rating DECIMAL(3,1),
    vote_count INTEGER,
    popularity DECIMAL(10,3),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 類型表
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 電影-類型關聯表
CREATE TABLE movie_genres (
    movie_id UUID REFERENCES movies(id),
    genre_id INTEGER REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);

-- 演員/導演表
CREATE TABLE people (
    id UUID PRIMARY KEY,
    tmdb_id INTEGER UNIQUE,
    name VARCHAR(200) NOT NULL,
    profile_path VARCHAR(500)
);

-- 電影-演職員關聯表
CREATE TABLE movie_credits (
    movie_id UUID REFERENCES movies(id),
    person_id UUID REFERENCES people(id),
    role VARCHAR(50), -- 'director', 'actor'
    character VARCHAR(200), -- 角色名（演員）
    order_num INTEGER, -- 排序
    PRIMARY KEY (movie_id, person_id, role)
);

-- 情緒標籤表（自訂）
CREATE TABLE mood_tags (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- 電影-情緒標籤關聯表
CREATE TABLE movie_moods (
    movie_id UUID REFERENCES movies(id),
    mood_id INTEGER REFERENCES mood_tags(id),
    weight DECIMAL(3,2), -- 0-1，表示關聯強度
    PRIMARY KEY (movie_id, mood_id)
);

-- 向量索引表（用於語義搜尋）
CREATE TABLE movie_embeddings (
    movie_id UUID PRIMARY KEY REFERENCES movies(id),
    embedding VECTOR(1536), -- OpenAI embedding 維度
    embedding_text TEXT, -- 用於生成 embedding 的文本
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 2.3.2 資料來源整合

**TMDB API 整合**
```python
import requests

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_movie_details(self, movie_id: int):
        url = f"{self.BASE_URL}/movie/{movie_id}"
        params = {"api_key": self.api_key, "language": "zh-TW"}
        response = requests.get(url, params=params)
        return response.json()
    
    def search_movies(self, query: str):
        url = f"{self.BASE_URL}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "language": "zh-TW"
        }
        response = requests.get(url, params=params)
        return response.json()
```

---

## 3. API 規格

### 3.1 端點定義

#### POST /api/recommend
獲取電影推薦

**請求**
```json
{
  "query": "我想看點輕鬆搞笑的",
  "limit": 10,
  "userId": "optional-user-id"
}
```

**回應**
```json
{
  "success": true,
  "data": {
    "intent": {
      "type": "mood",
      "emotion": "happy",
      "confidence": 0.95
    },
    "recommendations": [
      {
        "movie": {
          "id": "abc123",
          "title": "當幸福來敲門",
          "titleOriginal": "The Pursuit of Happyness",
          "posterUrl": "https://...",
          "releaseYear": 2006,
          "genres": ["劇情", "勵志"],
          "director": "蓋布瑞·穆奇諾",
          "cast": ["威爾·史密斯", "賈登·史密斯"],
          "rating": 8.0,
          "summary": "克里斯·加德納...",
          "runtime": 117
        },
        "matchScore": 0.87,
        "recommendationReason": "這是一部溫馨勵志的電影，能夠帶給您正能量和輕鬆的觀影體驗"
      }
    ],
    "totalCount": 8
  }
}
```

#### GET /api/movie/:id
獲取電影詳情

#### GET /api/health
健康檢查

---

## 4. 實作優先級

### Phase 1: MVP (4-6 週)
1. **Week 1-2: 基礎設施**
   - 設置資料庫
   - TMDB API 整合
   - 基本資料爬取和儲存

2. **Week 3-4: 核心功能**
   - NLU 模組（使用 LLM）
   - 基礎推薦引擎（精確搜尋 + 語義搜尋）
   - RESTful API

3. **Week 5-6: 前端介面**
   - 簡易 Web UI
   - 搜尋輸入
   - 推薦結果展示

### Phase 2: 優化 (4-6 週)
1. 情緒映射優化
2. 向量資料庫整合
3. 推薦理由生成優化
4. 效能優化和快取

### Phase 3: 擴展功能
1. 使用者系統
2. 觀影歷史
3. 個性化推薦

---

## 5. 效能指標

### 5.1 回應時間目標
- API 回應時間: < 500ms (不含 LLM 呼叫)
- 完整推薦流程: < 2s
- 資料庫查詢: < 100ms

### 5.2 快取策略
- 熱門查詢結果快取 (Redis, TTL: 1 hour)
- 電影詳情快取 (TTL: 24 hours)
- API 回應快取

### 5.3 擴展性
- 支援水平擴展
- 資料庫讀寫分離
- CDN 靜態資源

---

## 6. 安全性考量

### 6.1 API 安全
- Rate Limiting (每分鐘 60 次請求)
- API Key 驗證
- CORS 設定

### 6.2 資料安全
- 敏感資訊加密
- SQL Injection 防護
- XSS 防護

---

## 7. 測試策略

### 7.1 單元測試
- NLU 模組測試（意圖識別準確率）
- 推薦引擎測試

### 7.2 整合測試
- API 端點測試
- 資料庫整合測試

### 7.3 效能測試
- 負載測試
- 壓力測試

---

## 8. 部署架構

### 8.1 開發環境
- Docker Compose
- 本地開發環境

### 8.2 生產環境
- **選項 A**: Vercel (前端) + Railway/Render (後端)
- **選項 B**: AWS (EC2 + RDS + S3)
- **選項 C**: Google Cloud Platform

### 8.3 CI/CD
- GitHub Actions
- 自動化測試
- 自動部署

---

**文件版本**: 1.0  
**建立日期**: 2025-11-18  
**最後更新**: 2025-11-18  
**對應需求文件版本**: 1.0
