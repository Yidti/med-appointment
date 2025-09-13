# 醫療預約系統 Side Project

這是一個用於展示 Django、Vue.js 與 PostgreSQL 技術能力的 Side Project，嚴格遵循測試驅動開發（TDD）方法論，並透過 Docker 進行容器化部署。

## 核心技術棧

-   **後端**: Django, Django REST Framework
-   **前端**: Vue.js, Vue Router, Pinia
-   **資料庫**: PostgreSQL
-   **容器化**: Docker, Docker Compose
-   **網頁伺服器**: Nginx
-   **測試**: PyTest, Vitest, Playwright
-   **API 文件**: drf-yasg (Swagger UI)

---

## 本地開發與測試 (Local Docker-Based Development)

本專案推薦使用 Docker 作為主要的本地開發與測試環境，以確保與生產環境的一致性。

### 1. 環境準備

-   **Docker**: 請確認您已安裝並啟動 Docker Desktop。
-   **Node.js**: 前端相關指令（如 `npm run build`）需要 Node.js 環境。
-   **Git**: 用於版本控制。

### 2. 首次設定

1.  **Clone 專案**: `git clone https://github.com/Yidti/med-appointment.git`
2.  **進入專案目錄**: `cd med-appointment`
3.  **建立環境變數檔案**: 
    - 複製範本檔案：`cp .env.example .env`
    - 編輯 `.env` 檔案 (`nano .env`)，填入您的 Supabase **連線池 (Pooler)** 資訊和一個自訂的 `SECRET_KEY`。
4.  **建立 `.dockerignore` 檔案**：確保此檔案存在且內容正確，以避免建置映像檔時發生 `no space left on device` 的錯誤。
5.  **建置前端檔案**: 為了讓 Nginx 容器能提供服務，需要先建置一次前端專案。
    ```bash
    cd frontend && npm install && npm run build && cd ..
    ```

### 3. 啟動應用程式

在專案根目錄執行以下指令，即可一鍵啟動所有服務（Nginx, Gunicorn, Django）：

```bash
docker compose up --build
```
- 首次啟動或程式碼有變更時，建議加上 `--build` 參數。
- 若要在背景運行，請加上 `-d` 參數: `docker compose up -d`。

應用程式啟動後：
-   **前端網站**: [http://localhost](http://localhost)
-   **後端 API**: 可透過 `http://localhost/api/` 訪問
-   **後台管理**: [http://localhost/admin/](http://localhost/admin/)

### 4. 執行測試

在執行測試前，請確保您的 Docker 容器正在運行 (`docker compose up -d`)。

#### 後端單元測試

在一個**新的終端機**視窗中，執行以下指令。它會在 `backend` 容器內運行 `pytest`。

```bash
docker compose exec backend pytest
```

#### 前端單元測試

```bash
cd frontend
npm test
```

#### 端對端 (E2E) 測試

```bash
cd frontend
npx playwright test
```

---

## 部署 (Deployment)

本章節提供將此專案部署到雲端伺服器（以 GCP 為例）的流程。

### 1. 雲端主機設定

1.  **建立 VM**: 在 GCP Compute Engine 建立一台 `e2-micro` 的 Debian 系統 VM。為符合永久免費資格，區域請選擇指定的美國區域（如 `us-west1`）。
2.  **防火牆**: 建立 VM 時，勾選「允許 HTTP 流量」和「允許 HTTPS 流量」。
3.  **安裝環境**: 透過 SSH 登入主機，並安裝 Docker, Docker Compose, 和 Nginx。

### 2. 部署應用程式

1.  **Clone 專案**: `git clone https://github.com/Yidti/med-appointment.git`
2.  **進入目錄**: `cd med-appointment`
3.  **設定環境變數**: 建立並編輯 `.env` 檔案 (`nano .env`)，填入您的生產環境資料庫連線資訊和 `SECRET_KEY`。
4.  **啟動服務**: `sudo docker compose up -d --build`

### 3. 驗證部署

-   在瀏覽器中，輸入您 GCP 主機的「外部 IP 位址」，您應該能看到應用程式的前端介面。

---

## API 文件 (API Documentation)

當應用程式啟動後，您可以透過 `http://localhost/swagger/` 或 `http://localhost/redoc/` 存取 API 文件。
