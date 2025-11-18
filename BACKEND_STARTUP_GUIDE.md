# Backend 啟動流程指南

## 前置條件

- Python 3.13+ 已安裝
- TMDB API Key 已取得

## 一、環境設定

### 1.1 建立並設定 .env 檔案

```bash
# 複製環境變數範本
cd backend
Copy-Item .env.example .env
```

編輯 `backend/.env` 檔案，設定以下金鑰：

```env
# TMDB API
TMDB_API_KEY=your_api_key_here
TMDB_READ_ACCESS_TOKEN=your_access_token_here
```

**取得 TMDB API Key：**
1. 前往 https://www.themoviedb.org/signup 註冊帳號
2. 登入後進入 Settings → API
3. 申請 Developer API Key
4. 複製 API Key (v3 auth) 和 API Read Access Token

### 1.2 建立 Python 虛擬環境

```bash
# 在 backend 目錄下建立虛擬環境
python -m venv venv
```

### 1.3 啟動虛擬環境

```bash
# Windows PowerShell
.\venv\Scripts\activate

# 成功後會看到 (venv) 前綴
# (venv) PS E:\My_Repo\Github\20251118_CineMood\backend>
```

### 1.4 安裝依賴套件

```bash
pip install -r requirements.txt
```

**主要套件：**
- `fastapi==0.115.0` - Web 框架
- `uvicorn==0.32.0` - ASGI 伺服器
- `sqlalchemy==2.0.35` - ORM
- `requests==2.32.3` - HTTP 客戶端（TMDB API）
- `pydantic-settings==2.6.1` - 設定管理
- `python-dotenv==1.0.1` - 環境變數載入

## 二、啟動開發伺服器

### 2.1 標準啟動

```bash
# 確保在 backend 目錄且虛擬環境已啟動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**參數說明：**
- `app.main:app` - FastAPI 應用程式位置
- `--reload` - 檔案變更時自動重載（開發模式）
- `--host 0.0.0.0` - 監聽所有網路介面
- `--port 8000` - 監聽 8000 埠

### 2.2 啟動成功訊息

```
INFO:     Will watch for changes in these directories: ['E:\\My_Repo\\Github\\20251118_CineMood\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2.3 驗證伺服器運作

開啟瀏覽器訪問以下端點：

- **根路徑：** http://localhost:8000/
  ```json
  {
    "message": "Welcome to CineMood API",
    "version": "1.0.0",
    "docs": "/docs"
  }
  ```

- **健康檢查：** http://localhost:8000/health
  ```json
  {
    "status": "healthy"
  }
  ```

- **API 文件：** http://localhost:8000/docs
  - Swagger UI 互動式文件

- **ReDoc 文件：** http://localhost:8000/redoc
  - 替代文件介面

## 三、資料庫初始化

### 3.1 自動建立資料表

首次啟動時，FastAPI 會自動建立 SQLite 資料庫：

```
backend/
  └── cinemood.db  # SQLite 資料庫檔案（自動生成）
```

**資料表清單：**
1. `movies` - 電影資料
2. `genres` - 類型
3. `people` - 演員/導演
4. `mood_tags` - 情境標籤
5. `movie_genres` - 電影-類型關聯
6. `movie_credits` - 電影-演職人員關聯
7. `movie_moods` - 電影-情境關聯
8. `movie_embeddings` - 電影向量嵌入

### 3.2 驗證資料庫

```bash
# 使用 SQLite CLI（需另外安裝）
sqlite3 cinemood.db

# 列出所有資料表
.tables

# 查看資料表結構
.schema movies

# 離開
.quit
```

## 四、停止伺服器

### 4.1 停止 Uvicorn

在執行 `uvicorn` 的終端機按：

```
Ctrl + C
```

### 4.2 退出虛擬環境

```bash
deactivate
```

## 五、常見問題排解

### 5.1 Port 8000 已被占用

**錯誤訊息：**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): 通常一個通訊端位址 (通訊協定/網路位址/連接埠) 只允許使用一次。
```

**解決方法：**
```bash
# 方法 1: 使用其他埠
uvicorn app.main:app --reload --port 8001

# 方法 2: 找出占用程序並終止
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 5.2 找不到模組錯誤

**錯誤訊息：**
```
ModuleNotFoundError: No module named 'fastapi'
```

**解決方法：**
```bash
# 確認虛擬環境已啟動
.\venv\Scripts\activate

# 重新安裝依賴
pip install -r requirements.txt
```

### 5.3 TMDB API Key 錯誤

**錯誤訊息：**
```
Invalid API key
```

**解決方法：**
1. 檢查 `backend/.env` 檔案中 `TMDB_API_KEY` 是否正確
2. 確認 API Key 已在 TMDB 官網啟用
3. 使用 `TMDB_READ_ACCESS_TOKEN` 替代（較新的認證方式）

### 5.4 資料庫鎖定錯誤

**錯誤訊息：**
```
sqlite3.OperationalError: database is locked
```

**解決方法：**
```bash
# 關閉所有使用資料庫的程式
# 刪除資料庫重新建立
rm cinemood.db
# 重新啟動伺服器會自動建立新資料庫
```

## 六、開發模式快速啟動腳本

### 6.1 Windows PowerShell

建立 `backend/start.ps1`：

```powershell
# 啟動 CineMood Backend
Write-Host "Starting CineMood Backend..." -ForegroundColor Green

# 啟動虛擬環境
.\venv\Scripts\activate

# 啟動伺服器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**使用方式：**
```bash
cd backend
.\start.ps1
```

### 6.2 一鍵安裝腳本

建立 `backend/setup.ps1`：

```powershell
# CineMood Backend 安裝腳本
Write-Host "Setting up CineMood Backend..." -ForegroundColor Green

# 檢查 Python 版本
$pythonVersion = python --version
Write-Host "Python Version: $pythonVersion" -ForegroundColor Cyan

# 建立虛擬環境
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# 啟動虛擬環境
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\activate

# 安裝依賴
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# 複製環境變數範本
if (-Not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please edit .env file and add your TMDB API Key!" -ForegroundColor Red
}

Write-Host "Setup complete! Run '.\start.ps1' to start the server." -ForegroundColor Green
```

**使用方式：**
```bash
cd backend
.\setup.ps1
```

## 七、生產環境部署

### 7.1 使用 Gunicorn（Linux）

```bash
# 安裝 gunicorn
pip install gunicorn

# 啟動（4 個 worker）
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 7.2 環境變數設定

生產環境需修改 `.env`：

```env
ENVIRONMENT=production
DEBUG=False
```

### 7.3 使用 systemd（Linux）

建立 `/etc/systemd/system/cinemood.service`：

```ini
[Unit]
Description=CineMood FastAPI Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/backend/venv/bin"
ExecStart=/path/to/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

**啟動服務：**
```bash
sudo systemctl start cinemood
sudo systemctl enable cinemood
sudo systemctl status cinemood
```

## 八、下一步

### Phase 1 - Step 2: TMDB 資料同步

完成後端啟動驗證後，下一步是建立 TMDB 資料同步腳本：

1. 建立 `scripts/sync_tmdb.py` - TMDB API 整合
2. 同步 500-1000 部熱門電影資料
3. 驗證資料完整性

詳見 [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md) Phase 1 - Step 2。

---

**專案架構參考：**
- [BACKEND_ARCHITECTURE.md](./BACKEND_ARCHITECTURE.md) - 後端分層架構
- [DATABASE_ER_DIAGRAM.md](./DATABASE_ER_DIAGRAM.md) - 資料庫設計
- [Technical-Specification.md](./Technical-Specification.md) - 技術規格
