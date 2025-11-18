# CineMood Backend Architecture

CineMood 後端採用 **Layered Architecture (分層架構)**，參考 PilotX 的設計模式，遵循 Clean Architecture 原則。

## 🏗️ 架構設計

### 分層結構

```
┌─────────────────────────────────────────────────────────┐
│           API Layer (HTTP Endpoints)                    │  ← recommendation_api.py, movie_api.py
├─────────────────────────────────────────────────────────┤
│           Service Layer (Business Logic)                │  ← nlu_service.py, recommendation_service.py
├─────────────────────────────────────────────────────────┤
│        Repository Layer (Database CRUD)                 │  ← movie_repository.py, genre_repository.py
├─────────────────────────────────────────────────────────┤
│           Model Layer (ORM Models)                      │  ← movie_model.py, genre_model.py
└─────────────────────────────────────────────────────────┘
```

### 依賴方向

```
API Layer → Service Layer → Repository Layer → Model Layer → Database
```

**原則**: 每一層只能依賴下一層，不能跨層或反向依賴。

---

## 📁 完整檔案結構

```
backend/
├── app/
│   ├── models/                          # Model Layer (Database ORM Models)
│   │   ├── __init__.py
│   │   ├── movie_model.py               # Movie 電影表
│   │   ├── genre_model.py               # Genre 類型表
│   │   ├── person_model.py              # Person 演職員表
│   │   ├── mood_tag_model.py            # MoodTag 情緒標籤表
│   │   ├── movie_genre_model.py         # MovieGenre 電影-類型關聯表
│   │   ├── movie_credit_model.py        # MovieCredit 電影-演職員關聯表
│   │   ├── movie_mood_model.py          # MovieMood 電影-情緒關聯表
│   │   └── movie_embedding_model.py     # MovieEmbedding 電影向量表
│   │
│   ├── repositories/                    # Repository Layer (Database Operations)
│   │   ├── __init__.py
│   │   ├── movie_repository.py          # Movie CRUD operations
│   │   ├── genre_repository.py          # Genre CRUD operations
│   │   ├── person_repository.py         # Person CRUD operations
│   │   ├── mood_tag_repository.py       # MoodTag CRUD operations
│   │   └── recommendation_repository.py # 跨表查詢 (複雜查詢)
│   │
│   ├── services/                        # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   ├── nlu_service.py               # NLU 意圖解析服務
│   │   ├── recommendation_service.py    # 推薦引擎服務
│   │   ├── tmdb_service.py              # TMDB API 整合服務
│   │   ├── ollama_service.py            # Ollama LLM 整合服務
│   │   └── embedding_service.py         # 向量生成服務
│   │
│   ├── api/                             # API Layer (HTTP Endpoints)
│   │   ├── __init__.py
│   │   ├── recommendation_api.py        # POST /api/v1/recommend
│   │   ├── movie_api.py                 # GET /api/v1/movie/{id}
│   │   └── health_api.py                # GET /api/v1/health
│   │
│   ├── schemas/                         # Pydantic Schemas (Request/Response)
│   │   ├── __init__.py
│   │   ├── recommendation_schema.py     # 推薦請求/回應模型
│   │   ├── movie_schema.py              # 電影資料模型
│   │   └── nlu_schema.py                # NLU 解析結果模型
│   │
│   ├── core/                            # Core Configuration
│   │   ├── __init__.py
│   │   └── config.py                    # Settings & Environment
│   │
│   ├── db/                              # Database
│   │   ├── __init__.py
│   │   └── session.py                   # Database session & Base
│   │
│   ├── dependencies.py                  # Dependency Injection
│   └── main.py                          # FastAPI Application
│
├── requirements.txt                     # Python Dependencies
├── .env                                 # Environment Variables
└── .gitignore
```

---

## 🔄 資料流向

### 1. 電影推薦流程

```
POST /api/v1/recommend
    ↓
recommendation_api.get_recommendations()
    ↓
recommendation_service.recommend()
    ├─→ nlu_service.parse_intent()        # 解析使用者意圖
    │   └─→ ollama_service.chat()          # LLM 意圖分析
    ├─→ recommendation_repository.search() # 根據意圖類型查詢
    │   ├─→ exact_search()                 # 精確搜尋
    │   ├─→ semantic_search()              # 語義搜尋
    │   └─→ mood_based_search()            # 情緒搜尋
    └─→ embedding_service.encode()         # 生成查詢向量
    ↓
Return MovieRecommendation[]
```

### 2. 取得電影詳情流程

```
GET /api/v1/movie/{id}
    ↓
movie_api.get_movie()
    ↓
movie_repository.get_movie_by_id()
    ├─→ movie_model.query()
    ├─→ JOIN genres (透過 movie_genres)
    ├─→ JOIN people (透過 movie_credits)
    └─→ JOIN mood_tags (透過 movie_moods)
    ↓
Return Movie (with genres, cast, director, moods)
```

### 3. TMDB 資料同步流程

```
Background Task / Manual Trigger
    ↓
tmdb_service.sync_movies()
    ├─→ tmdb_service.search_movies()       # 呼叫 TMDB API
    ├─→ movie_repository.create_movie()    # 儲存電影
    ├─→ genre_repository.create_or_get()   # 建立類型
    ├─→ person_repository.create_or_get()  # 建立演員
    └─→ embedding_service.generate()       # 生成向量
    ↓
Save to Database
```

---

## 📦 各層職責

### 1. Model Layer (模型層)

**職責**: 定義資料庫表結構

**檔案**:
- `movie_model.py` - Movie 表 (電影基本資訊)
- `genre_model.py` - Genre 表 (電影類型)
- `person_model.py` - Person 表 (演員、導演)
- `mood_tag_model.py` - MoodTag 表 (情緒標籤)
- `movie_genre_model.py` - MovieGenre 表 (電影-類型關聯)
- `movie_credit_model.py` - MovieCredit 表 (電影-演職員關聯)
- `movie_mood_model.py` - MovieMood 表 (電影-情緒關聯)
- `movie_embedding_model.py` - MovieEmbedding 表 (電影向量)

**特點**:
- 使用 SQLAlchemy ORM
- 定義表之間的關聯關係
- 不包含業務邏輯

**範例**:
```python
# movie_model.py
from sqlalchemy import Column, String, Integer, Date, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tmdb_id = Column(Integer, unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    title_original = Column(String(500))
    release_date = Column(Date)
    runtime = Column(Integer)
    overview = Column(Text)
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    rating = Column(DECIMAL(3, 1))
    vote_count = Column(Integer)
    popularity = Column(DECIMAL(10, 3))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    genres = relationship("MovieGenre", back_populates="movie")
    credits = relationship("MovieCredit", back_populates="movie")
    moods = relationship("MovieMood", back_populates="movie")
    embedding = relationship("MovieEmbedding", back_populates="movie", uselist=False)
```

---

### 2. Repository Layer (資料庫層)

**職責**: 執行資料庫 CRUD 操作

**檔案**:
- `movie_repository.py` - Movie CRUD
- `genre_repository.py` - Genre CRUD
- `person_repository.py` - Person CRUD
- `mood_tag_repository.py` - MoodTag CRUD
- `recommendation_repository.py` - 複雜跨表查詢

**特點**:
- 只知道 Database Session 和 Model
- 提供簡單的 CRUD 方法
- 不包含業務邏輯

**範例**:
```python
# movie_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.movie_model import Movie
from app.models.genre_model import Genre

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_movie_by_id(self, movie_id: str) -> Optional[Movie]:
        """根據 ID 取得電影"""
        return self.db.query(Movie).filter(Movie.id == movie_id).first()
    
    def get_movie_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]:
        """根據 TMDB ID 取得電影"""
        return self.db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
    
    def search_movies(self, query: str, limit: int = 10) -> List[Movie]:
        """模糊搜尋電影標題"""
        return self.db.query(Movie)\
            .filter(Movie.title.contains(query))\
            .limit(limit).all()
    
    def create_movie(self, movie_data: dict) -> Movie:
        """建立電影"""
        movie = Movie(**movie_data)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
```

---

### 3. Service Layer (服務層)

**職責**: 實現業務邏輯

**檔案**:
- `nlu_service.py` - NLU 意圖解析
- `recommendation_service.py` - 推薦引擎
- `tmdb_service.py` - TMDB API 整合
- `ollama_service.py` - Ollama LLM 整合
- `embedding_service.py` - 向量生成

**特點**:
- 只依賴 Repository，不直接操作資料庫
- 處理複雜的業務流程
- 協調多個 Repository 和外部服務

**範例**:
```python
# recommendation_service.py
from typing import List
from app.repositories.movie_repository import MovieRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.nlu_service import NLUService
from app.services.embedding_service import EmbeddingService
from app.schemas.recommendation_schema import MovieRecommendation

class RecommendationService:
    def __init__(
        self,
        movie_repo: MovieRepository,
        recommendation_repo: RecommendationRepository,
        nlu_service: NLUService,
        embedding_service: EmbeddingService
    ):
        self.movie_repo = movie_repo
        self.recommendation_repo = recommendation_repo
        self.nlu_service = nlu_service
        self.embedding_service = embedding_service
    
    def recommend(self, query: str, limit: int = 10) -> List[MovieRecommendation]:
        """根據查詢推薦電影"""
        # 1. 解析使用者意圖
        intent = self.nlu_service.parse_intent(query)
        
        # 2. 根據意圖類型選擇搜尋策略
        if intent.intent_type == "exact":
            movies = self.recommendation_repo.exact_search(intent.entities, limit)
        elif intent.intent_type == "mood":
            movies = self.recommendation_repo.mood_based_search(intent.mood, limit)
        elif intent.intent_type == "fuzzy" or intent.intent_type == "question":
            # 語義搜尋
            query_vector = self.embedding_service.encode(intent.search_query)
            movies = self.recommendation_repo.semantic_search(query_vector, limit)
        
        # 3. 生成推薦理由
        recommendations = []
        for movie in movies:
            reason = self._generate_reason(movie, intent)
            recommendations.append(MovieRecommendation(
                movie=movie,
                match_score=0.85,  # TODO: 實際計算相似度
                recommendation_reason=reason
            ))
        
        return recommendations
    
    def _generate_reason(self, movie, intent) -> str:
        """生成推薦理由 (使用 LLM)"""
        # TODO: 使用 Ollama 生成推薦理由
        return f"這部電影符合您的需求"
```

---

### 4. API Layer (API 層)

**職責**: 處理 HTTP 請求和響應

**檔案**:
- `recommendation_api.py` - 推薦端點
- `movie_api.py` - 電影詳情端點
- `health_api.py` - 健康檢查端點

**特點**:
- 只依賴 Service，不直接操作資料庫或 Repository
- 處理 HTTP 驗證、錯誤處理
- 轉換 HTTP 請求到 Service 調用

**範例**:
```python
# recommendation_api.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.recommendation_schema import (
    RecommendationRequest,
    RecommendationResponse
)
from app.services.recommendation_service import RecommendationService
from app.dependencies import get_recommendation_service

router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """獲取電影推薦"""
    try:
        recommendations = service.recommend(
            query=request.query,
            limit=request.limit
        )
        
        return RecommendationResponse(
            success=True,
            data={
                "recommendations": recommendations,
                "total_count": len(recommendations)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🔌 依賴注入 (Dependency Injection)

使用 `dependencies.py` 統一管理依賴注入:

```python
# dependencies.py
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.repositories.movie_repository import MovieRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.nlu_service import NLUService
from app.services.recommendation_service import RecommendationService
from app.services.ollama_service import OllamaService
from app.services.embedding_service import EmbeddingService

# Repository Dependencies
def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    return MovieRepository(db)

def get_recommendation_repository(db: Session = Depends(get_db)) -> RecommendationRepository:
    return RecommendationRepository(db)

# Service Dependencies
def get_ollama_service() -> OllamaService:
    return OllamaService()

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

def get_nlu_service(
    ollama_service: OllamaService = Depends(get_ollama_service)
) -> NLUService:
    return NLUService(ollama_service)

def get_recommendation_service(
    movie_repo: MovieRepository = Depends(get_movie_repository),
    recommendation_repo: RecommendationRepository = Depends(get_recommendation_repository),
    nlu_service: NLUService = Depends(get_nlu_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> RecommendationService:
    return RecommendationService(
        movie_repo,
        recommendation_repo,
        nlu_service,
        embedding_service
    )
```

---

## ✅ 架構優勢

### 1. **單一職責原則 (SRP)**
- 每個類別只負責一件事
- Movie、Genre、Person 等各自獨立管理

### 2. **依賴反轉原則 (DIP)**
- 高層模組不依賴低層模組
- Service 依賴 Repository 介面，不依賴具體實作

### 3. **開放封閉原則 (OCP)**
- 對擴展開放：新增功能只需添加新的 Service 或 Repository
- 對修改封閉：現有程式碼不需要修改

### 4. **可測試性**
- 每一層都可以獨立測試
- 可以 Mock Repository 來測試 Service
- 可以 Mock Service 來測試 API

### 5. **可維護性**
- 清晰的結構，容易找到程式碼
- 職責分離，修改影響範圍小
- 檔案命名一致，易於理解

---

## 🔧 擴展指南

### 添加新功能 - 以「使用者評分」為例

1. **Model Layer**: 創建 `user_rating_model.py`
```python
class UserRating(Base):
    __tablename__ = "user_ratings"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    movie_id = Column(String(36), ForeignKey("movies.id"))
    rating = Column(Integer)
```

2. **Repository Layer**: 創建 `user_rating_repository.py`
```python
class UserRatingRepository:
    def __init__(self, db: Session):
        self.db = db
    def create_rating(self, user_id, movie_id, rating): ...
```

3. **Service Layer**: 創建 `user_rating_service.py`
```python
class UserRatingService:
    def __init__(self, repository: UserRatingRepository):
        self.repository = repository
    def rate_movie(self, user_id, movie_id, rating): ...
```

4. **API Layer**: 創建 `user_rating_api.py`
```python
@router.post("/movies/{movie_id}/rate")
def rate_movie(service: UserRatingService = Depends(get_user_rating_service)):
    return service.rate_movie(...)
```

5. **Dependencies**: 更新 `dependencies.py`
```python
def get_user_rating_service(repo = Depends(get_user_rating_repository)):
    return UserRatingService(repo)
```

6. **Main**: 註冊路由
```python
app.include_router(user_rating_api.router, prefix="/api/v1", tags=["ratings"])
```

---

## 📚 參考資料

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [PilotX Backend Architecture](../pilot_x/ARCHITECTURE.md)

---

**建立日期**: 2025-11-18  
**版本**: 1.0  
**對應技術規格文件版本**: 1.0
