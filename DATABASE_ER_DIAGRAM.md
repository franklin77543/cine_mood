# CineMood Database ER Diagram

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CineMood Database Schema                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│      movies          │
├──────────────────────┤
│ PK  id (UUID)        │
│ UK  tmdb_id (INT)    │
│     title            │
│     title_original   │
│     release_date     │
│     runtime          │
│     overview         │
│     poster_path      │
│     backdrop_path    │
│     rating           │
│     vote_count       │
│     popularity       │
│     created_at       │
│     updated_at       │
└──────────────────────┘
         │
         │ 1
         │
         ├─────────────────────────────────────────┐
         │                                         │
         │ N                                       │ N
         │                                         │
┌────────▼──────────┐                    ┌────────▼──────────┐
│  movie_genres     │                    │  movie_credits    │
├───────────────────┤                    ├───────────────────┤
│ PK  movie_id (FK) │                    │ PK  movie_id (FK) │
│ PK  genre_id (FK) │                    │ PK  person_id(FK) │
└───────────────────┘                    │ PK  role          │
         │                               │     character     │
         │ N                             │     order_num     │
         │                               └───────────────────┘
         │ 1                                      │
         │                                        │ N
┌────────▼──────────┐                             │
│     genres        │                             │ 1
├───────────────────┤                             │
│ PK  id (SERIAL)   │                    ┌────────▼──────────┐
│ UK  name          │                    │      people       │
└───────────────────┘                    ├───────────────────┤
                                         │ PK  id (UUID)     │
                                         │ UK  tmdb_id (INT) │
         ┌───────────────────────────────│     name          │
         │                               │     profile_path  │
         │ 1                             └───────────────────┘
         │
         │ N
┌────────▼──────────┐
│   movie_moods     │
├───────────────────┤
│ PK  movie_id (FK) │
│ PK  mood_id (FK)  │
│     weight        │
└───────────────────┘
         │
         │ N
         │
         │ 1
         │
┌────────▼──────────┐
│    mood_tags      │
├───────────────────┤
│ PK  id (SERIAL)   │
│ UK  tag           │
│     description   │
└───────────────────┘


         ┌───────────────────────────────┐
         │                               │
         │ 1                             │ 1
         │                               │
┌────────▼──────────┐           ┌────────▼──────────────┐
│      movies       │           │  movie_embeddings     │
│  (Same as above)  │───────────│  (1:1 Relationship)   │
└───────────────────┘           ├───────────────────────┤
                                │ PK  movie_id (FK)     │
                                │     embedding         │
                                │     embedding_text    │
                                │     created_at        │
                                └───────────────────────┘
```

## 實體說明

### 1. movies (電影主表)
**用途**: 儲存電影基本資訊
- **主鍵**: `id` (UUID) - 內部唯一識別碼
- **唯一鍵**: `tmdb_id` - TMDB API 的電影 ID
- **關聯**: 
  - 一對多 → `movie_genres` (電影可有多個類型)
  - 一對多 → `movie_credits` (電影可有多個演職員)
  - 一對多 → `movie_moods` (電影可有多個情緒標籤)
  - 一對一 → `movie_embeddings` (每部電影有一個向量表示)

### 2. genres (類型表)
**用途**: 儲存電影類型 (動作、喜劇、劇情等)
- **主鍵**: `id` (SERIAL)
- **唯一鍵**: `name` - 類型名稱
- **關聯**: 透過 `movie_genres` 與 `movies` 多對多

### 3. movie_genres (電影-類型關聯表)
**用途**: 建立電影與類型的多對多關係
- **複合主鍵**: (`movie_id`, `genre_id`)
- **關聯**: 
  - 多對一 → `movies`
  - 多對一 → `genres`

### 4. people (演職員表)
**用途**: 儲存演員、導演等人員資訊
- **主鍵**: `id` (UUID)
- **唯一鍵**: `tmdb_id` - TMDB API 的人員 ID
- **關聯**: 透過 `movie_credits` 與 `movies` 多對多

### 5. movie_credits (電影-演職員關聯表)
**用途**: 建立電影與演職員的多對多關係,記錄角色資訊
- **複合主鍵**: (`movie_id`, `person_id`, `role`)
- **欄位**:
  - `role`: 'director' (導演) 或 'actor' (演員)
  - `character`: 角色名稱 (僅演員有值)
  - `order_num`: 演員排序 (主演排前面)
- **關聯**:
  - 多對一 → `movies`
  - 多對一 → `people`

### 6. mood_tags (情緒標籤表)
**用途**: 儲存預定義的情緒標籤 (開心、悲傷、刺激等)
- **主鍵**: `id` (SERIAL)
- **唯一鍵**: `tag` - 標籤名稱
- **關聯**: 透過 `movie_moods` 與 `movies` 多對多

### 7. movie_moods (電影-情緒標籤關聯表)
**用途**: 建立電影與情緒標籤的多對多關係,帶權重
- **複合主鍵**: (`movie_id`, `mood_id`)
- **欄位**:
  - `weight`: 0-1 之間的小數,表示該情緒與電影的關聯強度
- **關聯**:
  - 多對一 → `movies`
  - 多對一 → `mood_tags`

### 8. movie_embeddings (電影向量表)
**用途**: 儲存電影的語義向量表示,用於相似度搜尋
- **主鍵**: `movie_id` (FK) - 與 movies 一對一
- **欄位**:
  - `embedding`: VECTOR(384) - 使用 paraphrase-multilingual-MiniLM-L12-v2 (384維)
  - `embedding_text`: 用於生成向量的原始文本 (標題+簡介+類型等)
- **關聯**: 一對一 → `movies`

---

## 關聯總結

### 一對多關係 (1:N)
1. `movies` → `movie_genres` (一部電影多個類型)
2. `movies` → `movie_credits` (一部電影多個演職員)
3. `movies` → `movie_moods` (一部電影多個情緒標籤)
4. `genres` → `movie_genres` (一個類型對應多部電影)
5. `people` → `movie_credits` (一個人參與多部電影)
6. `mood_tags` → `movie_moods` (一個情緒對應多部電影)

### 一對一關係 (1:1)
1. `movies` ↔ `movie_embeddings` (一部電影一個向量)

### 多對多關係 (N:M)
透過中間表實現:
1. `movies` ↔ `genres` (透過 `movie_genres`)
2. `movies` ↔ `people` (透過 `movie_credits`)
3. `movies` ↔ `mood_tags` (透過 `movie_moods`)

---

## 索引建議

### 主要查詢索引
```sql
-- movies 表
CREATE INDEX idx_movies_tmdb_id ON movies(tmdb_id);
CREATE INDEX idx_movies_rating ON movies(rating DESC);
CREATE INDEX idx_movies_popularity ON movies(popularity DESC);
CREATE INDEX idx_movies_release_date ON movies(release_date DESC);

-- people 表
CREATE INDEX idx_people_name ON people(name);
CREATE INDEX idx_people_tmdb_id ON people(tmdb_id);

-- movie_credits 表
CREATE INDEX idx_credits_movie_id ON movie_credits(movie_id);
CREATE INDEX idx_credits_person_id ON movie_credits(person_id);
CREATE INDEX idx_credits_role ON movie_credits(role);

-- movie_genres 表
CREATE INDEX idx_movie_genres_genre_id ON movie_genres(genre_id);

-- movie_moods 表
CREATE INDEX idx_movie_moods_mood_id ON movie_moods(mood_id);
CREATE INDEX idx_movie_moods_weight ON movie_moods(weight DESC);

-- movie_embeddings 表
-- 向量相似度搜尋索引 (使用 ChromaDB 不需要在 SQLite 建立)
```

---

## 資料流範例

### 1. 搜尋電影 "湯姆漢克斯的電影"
```
1. NLU 模組識別 → entities: {actor: "湯姆漢克斯"}
2. 查詢流程:
   people (name LIKE '%湯姆漢克斯%')
   → movie_credits (role='actor')
   → movies
   → JOIN movie_genres, genres (取得類型)
   → JOIN movie_moods, mood_tags (取得情緒標籤)
```

### 2. 情緒搜尋 "我想看點輕鬆的"
```
1. NLU 模組識別 → mood: {emotion: "happy", intensity: 0.8}
2. 查詢流程:
   mood_tags (tag='happy')
   → movie_moods (weight > 0.6)
   → movies (rating > 7.0)
   → JOIN genres (篩選 comedy, animation 類型)
```

### 3. 語義搜尋 "關於友情和成長的電影"
```
1. 生成查詢向量:
   embedding_model.encode("關於友情和成長的電影")
2. 查詢流程:
   ChromaDB.similarity_search(query_embedding, top_k=10)
   → 返回相似 movie_id 列表
   → movies (WHERE id IN (...))
   → JOIN 取得完整電影資訊
```

---

## 資料庫大小估算

### 假設 10,000 部電影
- `movies`: 10,000 rows × ~2KB = ~20MB
- `genres`: ~30 rows × 0.1KB = ~3KB
- `movie_genres`: 10,000 × 3 genres = 30,000 rows × 0.05KB = ~1.5MB
- `people`: ~50,000 rows × 0.5KB = ~25MB
- `movie_credits`: 10,000 × 20 credits = 200,000 rows × 0.1KB = ~20MB
- `mood_tags`: ~20 rows × 0.1KB = ~2KB
- `movie_moods`: 10,000 × 3 moods = 30,000 rows × 0.05KB = ~1.5MB
- `movie_embeddings`: 10,000 rows × 1.5KB (384維) = ~15MB

**總計**: ~83MB (不含索引和 ChromaDB)

---

**建立日期**: 2025-11-18  
**版本**: 1.0  
**對應技術規格文件版本**: 1.0
