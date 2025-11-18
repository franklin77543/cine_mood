# CineMood 開發路線圖

## 📋 開發策略

採用**由下而上 (Bottom-Up)** 的開發方式：
1. 先建立穩固的資料層
2. 再建立可靠的 API 層
3. 然後整合 AI 功能
4. 最後開發前端介面

這樣可以確保每一層都經過充分測試，降低後續整合問題。

---

## 🎯 Phase 1: 資料層建立 (Data Layer)

**目標**: 建立完整的資料庫結構，並從 TMDB 同步電影資料

### ✅ Task 1.1: 建立專案結構
- [ ] 建立 `backend/` 目錄結構
- [ ] 建立所有必要的子目錄 (models, repositories, services, api, schemas, core, db)
- [ ] 建立 `__init__.py` 檔案

### ✅ Task 1.2: 設定開發環境
- [ ] 建立 `requirements.txt`
  ```txt
  fastapi==0.115.0
  uvicorn[standard]==0.32.0
  sqlalchemy==2.0.35
  requests==2.32.3
  python-dotenv==1.0.1
  pydantic-settings==2.6.1
  ```
- [ ] 建立 Python 虛擬環境
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
  ```
- [ ] 建立 `.env` 檔案
  ```env
  # TMDB API
  TMDB_API_KEY=your_api_key_here
  TMDB_BASE_URL=https://api.themoviedb.org/3
  
  # Database
  DATABASE_URL=sqlite:///./cinemood.db
  
  # App Settings
  APP_NAME=CineMood
  DEBUG=True
  ```

### ✅ Task 1.3: 建立資料庫 Models (8個檔案)
- [ ] `models/movie_model.py` - Movie 電影主表
- [ ] `models/genre_model.py` - Genre 類型表
- [ ] `models/person_model.py` - Person 演職員表
- [ ] `models/mood_tag_model.py` - MoodTag 情緒標籤表
- [ ] `models/movie_genre_model.py` - MovieGenre 電影-類型關聯
- [ ] `models/movie_credit_model.py` - MovieCredit 電影-演職員關聯
- [ ] `models/movie_mood_model.py` - MovieMood 電影-情緒關聯
- [ ] `models/movie_embedding_model.py` - MovieEmbedding 電影向量表

### ✅ Task 1.4: 建立資料庫連線
- [ ] `db/session.py` - Database session 和 Base
- [ ] `core/config.py` - 設定檔管理

### ✅ Task 1.5: 建立 TMDB 同步腳本
- [ ] `scripts/sync_tmdb.py` - TMDB 資料同步腳本
  - 取得 TMDB API Key
  - 同步 500-1000 部熱門電影
  - 同步電影詳情 (類型、演員、導演)
  - 儲存到 SQLite

### ✅ Task 1.6: 執行資料同步
```powershell
cd backend
python scripts/sync_tmdb.py
```

### ✅ Task 1.7: 驗證資料完整性
- [ ] 使用 DB Browser for SQLite 開啟 `cinemood.db`
- [ ] 檢查各表資料：
  - `movies` 表: 應有 500-1000 筆
  - `genres` 表: 應有 ~20 筆 (動作、喜劇、劇情等)
  - `people` 表: 應有數千筆演員/導演
  - `movie_genres` 關聯表: 每部電影 2-4 個類型
  - `movie_credits` 關聯表: 每部電影 10+ 演職員
- [ ] 確認中文資料顯示正常
- [ ] 確認圖片路徑完整

**完成標準**: 
- ✅ 資料庫包含 500+ 部電影
- ✅ 所有關聯表資料正確
- ✅ 中文標題、簡介正常顯示

---

## 🎯 Phase 2: Backend API 建立 (API Layer)

**目標**: 建立基礎的 RESTful API，提供電影查詢功能

### ✅ Task 2.1: 建立 Repository Layer (資料庫操作)
- [ ] `repositories/movie_repository.py`
  - `get_movie_by_id()`
  - `get_movies()` - 分頁查詢
  - `search_movies(query)` - 標題模糊搜尋
  - `create_movie()`
- [ ] `repositories/genre_repository.py`
  - `get_all_genres()`
  - `get_genre_by_id()`
  - `create_or_get_genre()`
- [ ] `repositories/person_repository.py`
  - `get_person_by_id()`
  - `search_people(query)`
  - `create_or_get_person()`

### ✅ Task 2.2: 建立 Pydantic Schemas (請求/回應模型)
- [ ] `schemas/movie_schema.py`
  - `Movie` - 電影基本資訊
  - `MovieDetail` - 電影詳細資訊 (含演員、導演)
  - `MovieList` - 電影列表回應
- [ ] `schemas/genre_schema.py`
- [ ] `schemas/person_schema.py`

### ✅ Task 2.3: 建立 Service Layer (簡單業務邏輯)
- [ ] `services/movie_service.py`
  - `get_movie_detail()` - 取得電影完整資訊
  - `list_movies()` - 分頁列表
  - `search_movies()` - 搜尋功能

### ✅ Task 2.4: 建立 API Endpoints
- [ ] `api/movie_api.py`
  - `GET /api/v1/movies` - 電影列表 (分頁)
  - `GET /api/v1/movies/{id}` - 電影詳情
  - `GET /api/v1/movies/search?q=xxx` - 搜尋電影
- [ ] `api/genre_api.py`
  - `GET /api/v1/genres` - 所有類型
- [ ] `api/health_api.py`
  - `GET /api/v1/health` - 健康檢查

### ✅ Task 2.5: 建立依賴注入
- [ ] `dependencies.py` - 統一管理 Repository 和 Service 的依賴注入

### ✅ Task 2.6: 建立 FastAPI 應用
- [ ] `main.py`
  - 初始化 FastAPI
  - 設定 CORS
  - 註冊所有路由
  - 建立資料庫表

### ✅ Task 2.7: 啟動 Backend 伺服器
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ✅ Task 2.8: 測試 API 端點
使用 Postman 或 Thunder Client 測試：

- [ ] `GET http://localhost:8000/api/v1/health`
  - 預期: `{"status": "healthy"}`

- [ ] `GET http://localhost:8000/api/v1/movies?page=1&limit=10`
  - 預期: 返回 10 部電影列表

- [ ] `GET http://localhost:8000/api/v1/movies/{id}`
  - 預期: 返回完整電影資訊 (含類型、演員、導演)

- [ ] `GET http://localhost:8000/api/v1/movies/search?q=當幸福`
  - 預期: 返回「當幸福來敲門」等相關電影

- [ ] `GET http://localhost:8000/api/v1/genres`
  - 預期: 返回所有電影類型

- [ ] `GET http://localhost:8000/docs`
  - 預期: FastAPI 自動生成的 API 文件

**完成標準**:
- ✅ 所有 API 端點正常運作
- ✅ 資料正確回傳 (含中文)
- ✅ 關聯資料完整 (類型、演員、導演)
- ✅ API 文件自動生成

---

## 🎯 Phase 3: AI/NLU 整合 (AI Layer)

**目標**: 整合 Ollama LLM 和語義搜尋，實現智能推薦

### ✅ Task 3.1: 安裝 Ollama
- [ ] 下載並安裝 Ollama: https://ollama.ai/
- [ ] 下載 Llama 3.1 模型
  ```powershell
  ollama pull llama3.1:8b
  ollama list  # 確認模型已下載
  ```

### ✅ Task 3.2: 建立 Ollama Service
- [ ] `services/ollama_service.py`
  - `chat()` - 呼叫 Ollama API
  - `parse_json_response()` - 解析 LLM JSON 回應

### ✅ Task 3.3: 建立 NLU Service (意圖解析)
- [ ] `services/nlu_service.py`
  - `parse_intent(user_input)` - 解析使用者意圖
    - 精確搜尋: "我想看當幸福來敲門"
    - 模糊搜尋: "湯姆漢克斯的電影"
    - 情緒搜尋: "我想看點輕鬆搞笑的"
    - 問答: "有什麼好看的科幻片"
  - 返回 `ParsedIntent` (intentType, entities, mood, searchQuery)

### ✅ Task 3.4: 建立 Embedding Service (語義向量)
- [ ] 安裝 Sentence Transformers
  ```powershell
  pip install sentence-transformers
  ```
- [ ] `services/embedding_service.py`
  - 使用 `paraphrase-multilingual-MiniLM-L12-v2` (384維)
  - `encode(text)` - 生成文本向量
  - `batch_encode(texts)` - 批次生成向量

### ✅ Task 3.5: 生成電影向量
- [ ] `scripts/generate_embeddings.py`
  - 為所有電影生成向量
  - 向量來源: `title + overview + genres`
  - 儲存到 `movie_embeddings` 表

### ✅ Task 3.6: 建立 Recommendation Repository
- [ ] `repositories/recommendation_repository.py`
  - `exact_search(entities)` - 精確搜尋 (SQL LIKE)
  - `semantic_search(query_vector, top_k)` - 語義搜尋
  - `mood_based_search(mood, limit)` - 情緒搜尋

### ✅ Task 3.7: 建立 Recommendation Service
- [ ] `services/recommendation_service.py`
  - `recommend(query, limit)` - 主要推薦邏輯
    1. 呼叫 NLU Service 解析意圖
    2. 根據意圖類型選擇搜尋策略
    3. 呼叫對應的 Repository 方法
    4. 生成推薦理由 (使用 LLM)
    5. 返回 `MovieRecommendation[]`

### ✅ Task 3.8: 建立推薦 API
- [ ] `api/recommendation_api.py`
  - `POST /api/v1/recommend`
    - Request: `{"query": "我想看點輕鬆的", "limit": 10}`
    - Response: `MovieRecommendation[]` (含 matchScore, reason)
- [ ] `schemas/recommendation_schema.py`
  - `RecommendationRequest`
  - `RecommendationResponse`
  - `MovieRecommendation`
  - `ParsedIntent`

### ✅ Task 3.9: 測試推薦功能
測試不同類型的查詢：

- [ ] 精確搜尋
  ```json
  POST /api/v1/recommend
  {"query": "我想看當幸福來敲門", "limit": 5}
  ```

- [ ] 演員搜尋
  ```json
  POST /api/v1/recommend
  {"query": "湯姆漢克斯的電影", "limit": 10}
  ```

- [ ] 情緒搜尋
  ```json
  POST /api/v1/recommend
  {"query": "我想看點輕鬆搞笑的", "limit": 10}
  ```

- [ ] 語義搜尋
  ```json
  POST /api/v1/recommend
  {"query": "關於友情和成長的電影", "limit": 10}
  ```

**完成標準**:
- ✅ NLU 能正確識別 4 種意圖類型
- ✅ 語義搜尋返回相關電影
- ✅ 情緒搜尋推薦符合情緒的電影
- ✅ 每個推薦都有合理的推薦理由

---

## 🎯 Phase 4: Frontend 開發 (UI Layer)

**目標**: 建立 React 前端介面，提供良好的使用者體驗

### ✅ Task 4.1: 建立 React 專案
```powershell
cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

### ✅ Task 4.2: 安裝依賴
```powershell
# UI Framework
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p

# State Management
npm install zustand

# HTTP Client
npm install axios

# UI Components
npm install lucide-react
```

### ✅ Task 4.3: 設定 Tailwind CSS
- [ ] 設定 `tailwind.config.js`
- [ ] 設定 `index.css`
- [ ] 建立設計系統 (顏色、字型、間距)

### ✅ Task 4.4: 建立專案結構
```
frontend/src/
├── components/
│   ├── SearchInput/      # 搜尋輸入框
│   ├── MovieCard/        # 電影卡片
│   ├── MovieList/        # 電影列表
│   └── MovieDetail/      # 電影詳情
├── pages/
│   ├── HomePage.tsx      # 首頁
│   └── MovieDetailPage.tsx
├── services/
│   └── api.ts            # API 客戶端
├── store/
│   └── index.ts          # Zustand store
├── types/
│   └── index.ts          # TypeScript 類型
└── App.tsx
```

### ✅ Task 4.5: 建立 API Service
- [ ] `services/api.ts`
  - Axios 實例設定
  - `recommendApi.recommend(query)`
  - `movieApi.getDetail(id)`
  - `movieApi.search(query)`

### ✅ Task 4.6: 建立 Zustand Store
- [ ] `store/index.ts`
  - 搜尋查詢狀態
  - 推薦結果狀態
  - Loading 狀態
  - 錯誤狀態

### ✅ Task 4.7: 建立 UI 組件
- [ ] `SearchInput` - 搜尋輸入框 (自動調整高度)
- [ ] `MovieCard` - 電影卡片 (海報、標題、評分、類型)
- [ ] `MovieList` - 電影列表 (Grid 佈局)
- [ ] `MovieDetail` - 電影詳情頁 (完整資訊)

### ✅ Task 4.8: 建立頁面
- [ ] `HomePage` - 首頁 (搜尋框 + 推薦結果)
- [ ] `MovieDetailPage` - 電影詳情頁

### ✅ Task 4.9: 整合 Backend API
- [ ] 設定環境變數 `.env`
  ```env
  VITE_API_BASE_URL=http://localhost:8000/api/v1
  ```
- [ ] 測試 API 串接

### ✅ Task 4.10: 啟動 Frontend
```powershell
npm run dev
# 訪問 http://localhost:5173
```

### ✅ Task 4.11: 完整測試
- [ ] 搜尋功能正常
- [ ] 推薦結果顯示正確
- [ ] 電影卡片點擊進入詳情頁
- [ ] Loading 狀態顯示
- [ ] 錯誤處理正常
- [ ] 響應式設計 (手機/平板/桌面)

**完成標準**:
- ✅ 前端與後端 API 正常溝通
- ✅ 搜尋體驗流暢
- ✅ 電影資訊顯示完整
- ✅ UI 美觀且響應式

---

## 📊 進度追蹤

### Phase 1: 資料層 (預計 2-3 天)
- [ ] 專案結構建立
- [ ] Database Models 建立
- [ ] TMDB 資料同步
- [ ] 資料驗證

### Phase 2: Backend API (預計 3-4 天)
- [ ] Repository Layer
- [ ] Service Layer
- [ ] API Endpoints
- [ ] API 測試

### Phase 3: AI 整合 (預計 4-5 天)
- [ ] Ollama 設定
- [ ] NLU Service
- [ ] Embedding Service
- [ ] 推薦引擎
- [ ] 推薦 API

### Phase 4: Frontend (預計 5-7 天)
- [ ] React 專案設定
- [ ] UI 組件開發
- [ ] API 整合
- [ ] 完整測試

**總預計時間**: 14-19 天 (MVP)

---

## 🎯 當前狀態

**目前進度**: Phase 0 - 規劃完成

**下一步**: 開始 Phase 1 - Task 1.1

**準備事項**:
- [ ] 安裝 Python 3.13+
- [ ] 安裝 Node.js 18+
- [ ] 註冊 TMDB 帳號並取得 API Key
- [ ] 安裝 Ollama
- [ ] 安裝 DB Browser for SQLite (資料驗證用)

---

**文件版本**: 1.0  
**建立日期**: 2025-11-18  
**最後更新**: 2025-11-18
