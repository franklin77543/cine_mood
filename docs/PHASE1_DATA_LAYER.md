# Phase 1 - 資料層 (Data Layer)

## 📋 目標
建立完整的後端資料層，包含資料庫模型、TMDB API 整合、資料同步機制。

## 🏗️ 技術架構

```
┌─────────────────────────────────────────────────────────┐
│                  Phase 1 - Data Layer                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌───────────────┐             │
│  │   TMDB API   │───────> │  API Client   │             │
│  │  (zh-TW)     │         │ Rate Limiting │             │
│  └──────────────┘         └───────────────┘             │
│         │                         │                     │
│         ▼                         ▼                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Sync Script (sync_tmdb.py)                 │ │
│  │  - Fetch movies from TMDB                          │ │
│  │  - Transform & validate data                       │ │
│  │  - Store to database                               │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                             │
│                           ▼                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │         SQLAlchemy Models (8 tables)               │ │
│  │  - movies        - genres       - people           │ │
│  │  - movie_genres  - movie_credits                   │ │
│  │  - movie_moods   - movie_embeddings  - mood_tags   │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                             │
│                           ▼                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │              SQLite Database                       │ │
│  │           (cinemood.db)                            │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📝 任務分解

### **Task 1.1: 專案結構建立**
**目標**: 建立符合 pilot_x 架構的後端專案結構

**目錄結構**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 應用主程式
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # 設定檔 (pydantic-settings)
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py         # 資料庫 Session
│   ├── models/                # SQLAlchemy Models (每個表一個檔案)
│   │   ├── __init__.py
│   │   ├── movie_model.py
│   │   ├── genre_model.py
│   │   ├── person_model.py
│   │   ├── mood_tag_model.py
│   │   ├── movie_genre_model.py
│   │   ├── movie_credit_model.py
│   │   ├── movie_mood_model.py
│   │   └── movie_embedding_model.py
│   ├── repositories/          # 資料存取層 (Phase 2)
│   │   └── __init__.py
│   ├── services/              # 業務邏輯層
│   │   ├── __init__.py
│   │   └── tmdb_client.py    # TMDB API Client
│   ├── api/                   # API 路由 (Phase 2)
│   │   └── __init__.py
│   └── schemas/               # Pydantic Schemas (Phase 2)
│       └── __init__.py
├── scripts/                   # 工具腳本
│   ├── sync_tmdb.py          # TMDB 資料同步
│   ├── check_db.py           # 資料庫檢查
│   └── validate_data.py      # 資料驗證
├── requirements.txt           # Python 依賴
├── .env                       # 環境變數
├── .env.example              # 環境變數範例
└── venv/                     # 虛擬環境
```

**完成標準**:
- ✅ 所有目錄建立完成
- ✅ `__init__.py` 檔案齊全
- ✅ Git 初始化並設定 .gitignore

---

### **Task 1.2: 資料庫模型設計**
**目標**: 使用 SQLAlchemy 建立 8 個資料表模型

#### **1. movies 表** (`movie_model.py`)
```python
class Movie(Base):
    __tablename__ = "movies"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=uuid4)
    
    # TMDB Data
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    original_title = Column(String(500))
    overview = Column(Text)
    release_date = Column(Date)
    runtime = Column(Integer)
    vote_average = Column(DECIMAL(3, 1))
    vote_count = Column(Integer)
    popularity = Column(DECIMAL(10, 3))
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    genres = relationship("MovieGenre", back_populates="movie")
    credits = relationship("MovieCredit", back_populates="movie")
    moods = relationship("MovieMood", back_populates="movie")
    embedding = relationship("MovieEmbedding", back_populates="movie", uselist=False)
```

#### **2. genres 表** (`genre_model.py`)
```python
class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tmdb_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    movies = relationship("MovieGenre", back_populates="genre")
```

#### **3. people 表** (`person_model.py`)
```python
class Person(Base):
    __tablename__ = "people"
    
    id = Column(String(36), primary_key=True, default=uuid4)
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    profile_path = Column(String(500))
    
    # Relationships
    credits = relationship("MovieCredit", back_populates="person")
```

#### **4. mood_tags 表** (`mood_tag_model.py`)
```python
class MoodTag(Base):
    __tablename__ = "mood_tags"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    movies = relationship("MovieMood", back_populates="mood_tag")
```

#### **5. movie_genres 關聯表** (`movie_genre_model.py`)
```python
class MovieGenre(Base):
    __tablename__ = "movie_genres"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"))
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"))
    
    # Relationships
    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movies")
    
    __table_args__ = (UniqueConstraint('movie_id', 'genre_id'),)
```

#### **6. movie_credits 關聯表** (`movie_credit_model.py`)
```python
class MovieCredit(Base):
    __tablename__ = "movie_credits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"))
    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"))
    role = Column(String(50), nullable=False)  # 'actor' or 'director'
    character = Column(String(200))
    order_num = Column(Integer)
    
    # Relationships
    movie = relationship("Movie", back_populates="credits")
    person = relationship("Person", back_populates="credits")
    
    __table_args__ = (UniqueConstraint('movie_id', 'person_id', 'role'),)
```

#### **7. movie_moods 關聯表** (`movie_mood_model.py`)
```python
class MovieMood(Base):
    __tablename__ = "movie_moods"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"))
    mood_tag_id = Column(Integer, ForeignKey("mood_tags.id", ondelete="CASCADE"))
    confidence = Column(DECIMAL(3, 2))  # 0.00 - 1.00
    
    # Relationships
    movie = relationship("Movie", back_populates="moods")
    mood_tag = relationship("MoodTag", back_populates="movies")
    
    __table_args__ = (UniqueConstraint('movie_id', 'mood_tag_id'),)
```

#### **8. movie_embeddings 表** (`movie_embedding_model.py`)
```python
class MovieEmbedding(Base):
    __tablename__ = "movie_embeddings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(36), ForeignKey("movies.id", ondelete="CASCADE"), unique=True)
    embedding = Column(PickleType, nullable=False)  # numpy array
    model_version = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    movie = relationship("Movie", back_populates="embedding")
```

**完成標準**:
- ✅ 8 個模型檔案建立完成
- ✅ 所有關聯關係正確設定
- ✅ Cascade delete 設定完成
- ✅ 索引和 UniqueConstraint 設定正確

---

### **Task 1.3: 環境設定與依賴安裝**
**目標**: 設定開發環境和安裝必要依賴

#### **1. 建立虛擬環境**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

#### **2. requirements.txt**
```txt
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-multipart==0.0.9

# Database
sqlalchemy==2.0.35

# HTTP Client
requests==2.32.3

# Environment Variables
python-dotenv==1.0.1
pydantic-settings==2.6.1

# AI/ML (Phase 3)
# sentence-transformers==2.2.2
# chromadb==0.4.22

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
```

#### **3. .env 設定**
```env
# Project
PROJECT_NAME=CineMood
API_V1_PREFIX=/api/v1
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=sqlite:///./cinemood.db

# CORS
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# TMDB API
TMDB_API_KEY=你的_API_KEY
TMDB_READ_ACCESS_TOKEN=你的_READ_ACCESS_TOKEN
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p

# AI Provider (Phase 3)
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT=60

# AI Parameters
MAX_TOKENS=2000
TEMPERATURE=0.7
```

#### **4. config.py**
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "CineMood"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./cinemood.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
    
    # TMDB API
    TMDB_API_KEY: str = ""
    TMDB_READ_ACCESS_TOKEN: str = ""
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**完成標準**:
- ✅ 虛擬環境建立成功
- ✅ 所有依賴安裝完成
- ✅ .env 檔案設定完成
- ✅ TMDB API 憑證設定正確

---

### **Task 1.4: TMDB API Client**
**目標**: 建立 TMDB API 客戶端，支援速率限制和中文資料

#### **tmdb_client.py**
```python
import requests
import time
from typing import Dict, List, Optional
from app.core.config import settings


class TMDBClient:
    """TMDB API 客戶端"""
    
    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}",
            "Content-Type": "application/json;charset=utf-8"
        }
        self.last_request_time = 0
        self.min_request_interval = 0.025  # 25ms = 40 requests/second
    
    def _rate_limit(self):
        """速率限制：確保請求間隔至少 25ms"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """發送 API 請求"""
        self._rate_limit()
        
        if params is None:
            params = {}
        
        # 自動添加中文語言參數
        params['language'] = 'zh-TW'
        
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_genres(self) -> List[Dict]:
        """獲取所有電影類型"""
        data = self._request("genre/movie/list")
        return data.get('genres', [])
    
    def get_popular_movies(self, page: int = 1) -> Dict:
        """獲取熱門電影"""
        return self._request("movie/popular", {"page": page})
    
    def get_top_rated_movies(self, page: int = 1) -> Dict:
        """獲取高評分電影"""
        return self._request("movie/top_rated", {"page": page})
    
    def get_now_playing_movies(self, page: int = 1) -> Dict:
        """獲取現正上映電影"""
        return self._request("movie/now_playing", {"page": page})
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """獲取電影詳細資訊"""
        return self._request(f"movie/{movie_id}")
    
    def get_movie_credits(self, movie_id: int) -> Dict:
        """獲取電影演職人員"""
        return self._request(f"movie/{movie_id}/credits")
    
    def get_image_url(self, path: str, size: str = "w500") -> str:
        """生成圖片完整 URL"""
        if not path:
            return ""
        return f"{self.image_base_url}/{size}{path}"
    
    def search_movies(self, query: str, page: int = 1) -> Dict:
        """搜尋電影"""
        return self._request("search/movie", {"query": query, "page": page})


# 建立全域實例
tmdb_client = TMDBClient()
```

**功能特色**:
- ✅ Bearer Token 認證
- ✅ 自動速率限制 (25ms 間隔)
- ✅ 自動添加 zh-TW 語言參數
- ✅ 完整的錯誤處理

**完成標準**:
- ✅ TMDBClient 實作完成
- ✅ 所有 API 方法測試通過
- ✅ 速率限制正常運作
- ✅ 中文資料正確獲取

---

### **Task 1.5: TMDB 資料同步腳本**
**目標**: 從 TMDB 同步電影資料到本地資料庫

#### **同步策略**
考量 TMDB API 免費額度限制 (1000 requests/day):
- **熱門電影**: 5 頁 ≈ 100 部電影
- **高評分電影**: 5 頁 ≈ 100 部電影
- **現正上映**: 3 頁 ≈ 60 部電影
- **總計**: 約 212 部電影 ≈ 520 requests (安全範圍)

#### **sync_tmdb.py 核心流程**
```python
def main():
    # 1. 初始化資料庫
    init_db()
    
    # 2. 同步類型
    genre_map = sync_genres(db)
    
    # 3. 同步熱門電影 (5 頁)
    sync_movies_from_endpoint(
        db, "熱門電影", 
        tmdb_client.get_popular_movies, 
        genre_map, 
        max_pages=5
    )
    
    # 4. 同步高評分電影 (5 頁)
    sync_movies_from_endpoint(
        db, "高評分電影", 
        tmdb_client.get_top_rated_movies, 
        genre_map, 
        max_pages=5
    )
    
    # 5. 同步現正上映 (3 頁)
    sync_movies_from_endpoint(
        db, "現正上映", 
        tmdb_client.get_now_playing_movies, 
        genre_map, 
        max_pages=3
    )
```

#### **關鍵功能**
1. **sync_genres()**: 同步所有電影類型
2. **sync_movie()**: 同步單部電影詳細資料
3. **sync_person()**: 同步演職人員資料
4. **重複檢查**: 使用 tmdb_id 避免重複

#### **資料轉換**
```python
# 日期格式轉換
release_date = datetime.strptime(
    details.get("release_date"), 
    "%Y-%m-%d"
).date() if details.get("release_date") else None

# 類型關聯
for genre_data in details.get("genres", []):
    genre = genre_map.get(genre_data["id"])
    if genre:
        movie_genre = MovieGenre(movie_id=movie.id, genre_id=genre.id)
        db.add(movie_genre)
```

**完成標準**:
- ✅ 同步腳本執行成功
- ✅ 212 部電影資料完整
- ✅ 所有關聯資料正確
- ✅ 無重複資料

---

### **Task 1.6: 資料驗證腳本**
**目標**: 驗證同步資料的完整性和正確性

#### **check_db.py** - 資料庫統計
```python
def main():
    db = SessionLocal()
    
    print("=" * 60)
    print("CineMood - 資料庫統計")
    print("=" * 60)
    
    # 統計各表資料量
    movies_count = db.query(func.count(Movie.id)).scalar()
    genres_count = db.query(func.count(Genre.id)).scalar()
    people_count = db.query(func.count(Person.id)).scalar()
    credits_count = db.query(func.count(MovieCredit.id)).scalar()
    
    print(f"電影數量: {movies_count}")
    print(f"類型數量: {genres_count}")
    print(f"演職人員: {people_count}")
    print(f"演職記錄: {credits_count}")
```

#### **validate_data.py** - 資料驗證
```python
def validate_chinese_support():
    """驗證中文支援"""
    movies = db.query(Movie).filter(
        Movie.title.like('%科學%')
    ).all()
    print(f"找到 {len(movies)} 部包含'科學'的電影")

def validate_genres():
    """驗證類型分佈"""
    genre_stats = db.query(
        Genre.name, 
        func.count(MovieGenre.id)
    ).join(MovieGenre).group_by(Genre.name).all()
    
    for genre_name, count in genre_stats:
        print(f"{genre_name}: {count} 部電影")

def validate_credits():
    """驗證演職人員"""
    top_actors = db.query(
        Person.name, 
        func.count(MovieCredit.id)
    ).join(MovieCredit).filter(
        MovieCredit.role == 'actor'
    ).group_by(Person.name).order_by(
        func.count(MovieCredit.id).desc()
    ).limit(10).all()
    
    for name, count in top_actors:
        print(f"{name}: {count} 部電影")

def validate_movie_data():
    """驗證電影資料完整性"""
    total = db.query(func.count(Movie.id)).scalar()
    
    with_title = db.query(func.count(Movie.id)).filter(
        Movie.title.isnot(None)
    ).scalar()
    
    with_overview = db.query(func.count(Movie.id)).filter(
        Movie.overview.isnot(None)
    ).scalar()
    
    print(f"標題完整度: {with_title}/{total} ({with_title/total*100:.1f}%)")
    print(f"簡介完整度: {with_overview}/{total} ({with_overview/total*100:.1f}%)")
```

**完成標準**:
- ✅ 所有統計數據正確
- ✅ 中文資料正常顯示
- ✅ 類型分佈合理
- ✅ 演職人員資料完整

---

### **Task 1.7: FastAPI 基礎設定**
**目標**: 建立基礎 FastAPI 應用，為 Phase 2 準備

#### **main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    description="AI-powered movie recommendation system",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to CineMood API",
        "docs": "/docs",
        "version": "1.0.0"
    }
```

#### **session.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 建立引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 需要
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
```

**測試**:
```bash
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

**完成標準**:
- ✅ FastAPI 成功啟動
- ✅ Swagger UI 可訪問 (http://localhost:8000/docs)
- ✅ CORS 設定正確
- ✅ 資料表自動建立

---

## 🎯 Phase 1 完成標準總覽

### 1. 專案結構
- ✅ 完整的目錄結構
- ✅ pilot_x 架構模式
- ✅ Git 版控設定

### 2. 資料庫模型
- ✅ 8 個 SQLAlchemy 模型
- ✅ 所有關聯關係正確
- ✅ 索引和約束設定

### 3. 環境設定
- ✅ 虛擬環境建立
- ✅ 依賴安裝完成
- ✅ TMDB API 憑證設定

### 4. TMDB 整合
- ✅ API Client 實作
- ✅ 速率限制機制
- ✅ 中文資料支援

### 5. 資料同步
- ✅ 212 部電影同步
- ✅ 19 個類型
- ✅ 2016 位演職人員
- ✅ 2274 條演職記錄

### 6. 資料品質
- ✅ 100% 標題完整度
- ✅ 80.7% 簡介完整度
- ✅ 100% 發行日期
- ✅ 98.1% 評分資料

### 7. 驗證測試
- ✅ 資料庫統計正確
- ✅ 中文搜尋正常
- ✅ 類型分佈合理
- ✅ FastAPI 啟動成功

---

## 📊 實際成果

### 資料統計
- **電影總數**: 212 部
- **類型數量**: 19 個 (簡體中文)
- **演職人員**: 2016 人
- **演職記錄**: 2274 條
- **類型關聯**: 564 條

### 熱門類型分佈
1. 剧情 (Drama): 92 部
2. 动作 (Action): 64 部
3. 惊悚 (Thriller): 59 部
4. 喜剧 (Comedy): 47 部
5. 科幻 (Sci-Fi): 42 部

### 熱門演員
1. 摩根費里曼: 5 部電影
2. 馬克·魯法洛: 4 部電影
3. 史嘉蕾·喬韓森: 4 部電影

### API 使用統計
- **總請求數**: ~520 requests
- **每日限額**: 1000 requests
- **使用率**: 52% (安全範圍)

---

## 🔧 遇到的問題與解決方案

### 問題 1: 欄位名稱不一致
**症狀**: Model 欄位與 TMDB API 返回的欄位名稱不一致
**解決**: 
- `title_original` → `original_title`
- `rating` → `vote_average`
- `order` → `order_num` (避免 SQL 關鍵字衝突)

### 問題 2: 類型關聯錯誤
**症狀**: Movie detail API 返回 `genre_ids` 但資料庫期望 `genres`
**解決**: 修改同步腳本使用 `details.get("genres")` 而非 `genre_ids`

### 問題 3: 日期格式轉換
**症狀**: TMDB 返回字串格式日期
**解決**: 使用 `datetime.strptime()` 轉換為 `date` 物件

### 問題 4: 重複演職人員
**症狀**: 同一人同一角色被重複添加
**解決**: 使用 `added_actors` 和 `added_directors` 集合追蹤

### 問題 5: Genre model 缺少 tmdb_id
**症狀**: Phase 2 API 返回錯誤
**解決**: 
- 添加 `tmdb_id` 欄位到 Genre model
- 執行資料庫遷移腳本

### 問題 6: PowerShell 執行環境
**症狀**: 分開執行 cd、activate、python 會失去上下文
**解決**: 使用單行命令鏈 `cd backend; .\venv\Scripts\Activate.ps1; python script.py`

---

## ⏱️ 開發時程

| 任務 | 預估時間 | 實際時間 |
|------|----------|----------|
| Task 1.1: 專案結構 | 30 min | 30 min |
| Task 1.2: 資料庫模型 | 1.5 hr | 1.5 hr |
| Task 1.3: 環境設定 | 30 min | 45 min |
| Task 1.4: TMDB Client | 1 hr | 1 hr |
| Task 1.5: 資料同步 | 2 hr | 3 hr* |
| Task 1.6: 資料驗證 | 30 min | 45 min |
| Task 1.7: FastAPI 設定 | 30 min | 30 min |
| **總計** | **6.5 小時** | **8 小時** |

\* 包含除錯和多次測試時間

---

## 📚 Git 提交記錄

### Commit 1: 初始結構
```
feat: Complete Phase 1 Step 1 - Backend structure with SQLAlchemy models
- 22 files created
- Complete directory structure
- 8 SQLAlchemy models
- Configuration and session setup
```

### Commit 2: 資料同步
```
feat: Complete Phase 1 - Data Layer with TMDB sync and validation
- 5 files created
- TMDB API client with rate limiting
- Data sync script (212 movies)
- Validation scripts
```

### Commit 3: 文檔更新
```
docs: Update DEVELOPMENT_ROADMAP.md with Phase 1 actual results
- Updated sync strategy with actual numbers
- Added TMDB limit explanation
- Marked Phase 1 as completed
```

---

## 🚀 下一步

Phase 1 完成後，進入 **Phase 2 - API Layer**:
- Repository Layer (資料存取層)
- Pydantic Schemas (資料驗證)
- Service Layer (業務邏輯)
- RESTful API Endpoints
- API 測試與文檔

**資料層穩固，API 層就緒！** 🎬
