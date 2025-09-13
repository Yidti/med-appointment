# 醫療預約系統 Side Project

這是一個用於展示 Django、Vue.js 與 PostgreSQL 技術能力的 Side Project，嚴格遵循測試驅動開發（TDD）方法論，並模擬一個完整的產品開發流程。

## 核心技術棧

-   **後端**: Django, Django REST Framework
-   **前端**: Vue.js, Vue Router, Pinia
-   **資料庫**: PostgreSQL
-   **測試**: PyTest, Vitest, Playwright
-   **API 文件**: drf-yasg (Swagger UI)

---

## 開發環境設定 (Local Development Setup)

請依照以下步驟在您的本機環境中設定並執行此專案。

### 1. 環境準備

-   **Python**: 專案依賴的 `psycopg2-binary` 套件需要 C 語言編譯環境。為避免相容性問題，強烈建議使用 **Python 3.11**。
-   **Node.js**: 建議使用 18+ 版本。
-   **Docker**: 本地測試環境依賴 Docker 來啟動 PostgreSQL 資料庫。請確認您已安裝並啟動 Docker Desktop。

### 2. 後端設定

從專案根目錄開始：

```bash
# 1. 建立並啟動 Python 3.11 虛擬環境
# 確保您的 python 指令指向 Python 3.11
python -m venv venv
source venv/bin/activate # macOS/Linux
# .\venv\Scripts\activate # Windows

# 2. 安裝 Python 依賴套件
pip install -r requirements.txt

# 3. 執行資料庫遷移 (針對本地 Docker 測試資料庫)
# 在執行測試前，您需要一個運行的本地資料庫容器
# 請參考下方的「測試」章節來啟動它

# 4. 建立後台管理員帳號 (可選)
# 依提示設定您的 email 和密碼
python manage.py createsuperuser
```

### 3. 前端設定

```bash
# 進入 frontend 目錄
cd frontend

# 安裝 Node.js 依賴套件
npm install
```

### 4. 啟動應用程式

我們已設定好一鍵啟動指令，可同時運行前後端伺服器。

**注意**: 此指令會啟動後端，並嘗試連接到 `settings.py` 中設定的資料庫。在本地開發時，請確保您的 Docker PostgreSQL 容器正在運行。

```bash
# 確認您仍在 frontend 目錄下
cd frontend

# 執行啟動指令
npm run start
```

-   後端 API 將運行在 `http://localhost:8000`
-   前端網站將運行在 `http://localhost:5173`

---

## 測試

在執行任何測試前，請確保您沒有其他本地的 PostgreSQL 服務佔用 `5432` 連接埠。

### 啟動本地測試資料庫

所有測試都需要一個 PostgreSQL 資料庫。請執行以下指令來啟動一個 Docker 容器作為測試資料庫：

```bash
docker run --name med-postgres-test -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpassword -p 5432:5432 -d postgres
```

測試結束後，可以使用 `docker stop med-postgres-test && docker rm med-postgres-test` 來關閉並移除容器。

### 後端測試

```bash
# 確保虛擬環境已啟動，且測試資料庫容器正在運行
./venv/bin/pytest
```

### 前端單元/元件測試

```bash
cd frontend
npm test
```

### 端對端 (E2E) 測試

我們提供兩種執行 E2E 測試的方式：

**1. 便利腳本 (適合本地開發)**

此指令會自動處理資料庫遷移、啟動服務、執行測試和清理測試資料。我們已對其進行優化，但在某些情況下仍可能不穩定。

```bash
# 進入 frontend 目錄
cd frontend
npm run test:e2e
```

**2. 手動循序流程 (最穩定，適用於 CI/CD)**

如果便利腳本卡住，或在自動化環境中，請遵循此流程：

```bash
# 1. (手動) 確保測試資料庫容器正在運行

# 2. (手動) 在一個終端機視窗中，於專案根目錄啟動後端 (背景運行)
./venv/bin/python manage.py runserver &

# 3. (手動) 在另一個終端機視窗中，於 frontend 目錄啟動前端 (背景運行)
cd frontend
npm run dev &

# 4. 等待約 10 秒後，執行測試
cd frontend
npx playwright test

# 5. (手動) 測試結束後，使用 kill 指令關閉背景服務
```

### 遠端資料庫連線測試 (Remote Database Connection Test)

在部署到雲端平台前，您可以在本地驗證與遠端資料庫（例如 Supabase）的連線是否正常。本專案使用 `python-dotenv` 來管理環境變數。

1.  **建立 `.env` 檔案**: 在專案的根目錄（與 `manage.py` 同層）建立一個名為 `.env` 的檔案。

2.  **填寫變數**: 將您的遠端資料庫連線資訊填入 `.env` 檔案中，格式如下。`DYNO=1` 是必須的，它會觸發 `settings.py` 中的生產環境模式。

    ```dotenv
    # --- Production Environment Settings ---
    DYNO=1
    SECRET_KEY=your_production_secret_key_here

    # --- Database Settings (from Supabase or other provider) ---
    DB_HOST=your_remote_db_host
    DB_NAME=your_remote_db_name
    DB_USER=your_remote_db_user
    DB_PASSWORD=your_remote_db_password
    DB_PORT=your_remote_db_port

    # --- CORS Settings (your frontend domain) ---
    CORS_ALLOWED_ORIGINS=http://your_frontend_domain.com,http://localhost:5173
    ```

3.  **執行檢查**: 執行 Django 的 `check` 指令，它會嘗試連接資料庫。

    ```bash
    ./venv/bin/python manage.py check
    ```

4.  **驗證結果**: 如果您看到 `System check identified no issues (0 silenced).` 的訊息，代表連線成功。

> **⚠️ 安全警告**: `README.md` 中已將 `.env` 檔案加入 `.gitignore`。請再次確認，絕對不要將包含敏感資訊的 `.env` 檔案提交到版本控制系統。

---

## API 文件 (API Documentation)

當後端伺服器啟動後，您可以透過以下網址存取互動式的 API 文件：

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 部署 (Deployment)

本章節提供將此專案部署到雲端伺服器（以 GCP 為例）的完整流程。

### 1. 雲端主機設定

1.  **建立 VM 執行個體**: 在 GCP Compute Engine 上，建立一台 `e2-micro` 的 VM，為符合永久免費資格，區域請選擇指定的美國區域（如 `us-west1`）。作業系統選擇 **Debian** (例如 Debian 11 或 12)。
2.  **設定防火牆**: 建立 VM 時，務必勾選「允許 HTTP 流量」和「允許 HTTPS 流量」。
3.  **安裝環境**: 透過 SSH 登入主機，並安裝 Docker, Docker Compose, 和 Nginx。請參考 `GEMINI.md` 開發日誌中的詳細指令。

### 2. 部署應用程式

1.  **Clone 專案**: 在遠端主機的家目錄中，執行 `git clone https://github.com/Yidti/med-appointment.git`。
2.  **進入專案目錄**: `cd med-appointment`。
3.  **設定環境變數**: 
    - 在專案根目錄手動建立 `.env` 檔案：`nano .env`。
    - 參考 `README.md` 中的「遠端資料庫連線測試」章節，將所有必要的生產環境變數（資料庫連線資訊、SECRET_KEY 等）填入檔案中。
4.  **啟動服務**: 使用 Docker Compose 一鍵啟動所有服務。
    ```bash
    sudo docker compose up -d --build
    ```
    - `-d` 參數代表在背景運行。
    - `--build` 參數會強制 Docker 在啟動前，根據最新的 `Dockerfile` 重新建置映像檔。

### 3. 驗證部署

-   在瀏覽器中，輸入您 GCP 主機的「外部 IP 位址」。如果一切順利，您應該能看到 Vue.js 應用程式的前端介面。
-   您可以嘗試註冊、登入、預約，確認所有功能都與生產資料庫正常互動。