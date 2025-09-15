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

> **注意**: 雖然此指令方便，但在某些情況下，由於前後端服務啟動時序問題，可能會導致測試不穩定。若遇到 E2E 測試失敗，建議參考下方的「E2E 測試偵錯指南」採用更穩定的循序執行方式進行偵錯。

---

## E2E 測試偵錯指南 (E2E Test Debugging Guide)

當 E2E 測試失敗時，請按照以下步驟進行偵錯：

### 1. 優先使用穩定測試流程

若您是使用 `npm run test:e2e` (並行啟動) 遇到問題，請改用以下循序執行流程，以排除服務啟動時序導致的不穩定性。為了方便，我們已將這些步驟整合為一個 Shell Script (`run_e2e_local.sh`)：

```bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Seeding test data ---"
./venv/bin/python manage.py seed_test_doctor

echo "--- Starting backend server in background ---"
(./venv/bin/python manage.py migrate --no-input && ./venv/bin/python manage.py runserver) &
BACKEND_PID=$!
echo "Backend PIDs: $BACKEND_PID"

echo "--- Starting frontend server in background ---"
(cd frontend && npm run dev) &
FRONTEND_PID=$!
echo "Frontend PIDs: $FRONTEND_PID"

echo "--- Waiting for services to be ready ---"
npx wait-on http://localhost:5173 http://localhost:8000/api/doctors/

echo "--- Running Playwright E2E tests ---"
cd frontend && npx playwright test

echo "--- Cleaning up test data ---"
cd .. # Go back to root if playwright test changed directory
./venv/bin/python manage.py cleanup_test_data

echo "--- Stopping background servers ---"
kill $BACKEND_PID $FRONTEND_PID || true # Use || true to prevent script from exiting if a PID is already dead

echo "--- E2E tests completed successfully ---"
```

**如何使用**: 在專案根目錄下執行 `./run_e2e_local.sh`。

### 2. 檢查服務狀態

*   **確認伺服器是否運行**: 使用 `curl -I http://localhost:5173` 和 `curl -I http://localhost:8000/api/doctors/` 檢查前端和後端服務是否正常響應。
*   **檢查 `wait-on` 配置**: 確保 `wait-on` 指令中的 URL 正確，特別是後端 API 的路徑。

### 3. 分析錯誤日誌

*   **Playwright 測試報告**: 執行 `npx playwright show-report` 查看詳細的測試報告，了解具體的失敗步驟、截圖和錯誤訊息。
*   **瀏覽器控制台**: 在 Playwright 測試執行期間，檢查瀏覽器的開發者工具控制台，尋找前端相關的錯誤或警告。
*   **後端伺服器日誌**: 檢查後端 Django 伺服器的控制台輸出，尋找任何 API 處理錯誤、資料庫相關問題或伺服器啟動異常。即使是 `Broken pipe` 等看似無害的訊息，若頻繁出現或在關鍵操作時發生，也可能暗示潛在問題。
*   **前端開發伺服器日誌**: 檢查前端 Vite 伺服器的控制台輸出，尋找編譯或運行時錯誤。

### 4. 逐步偵錯

*   **使用 `page.pause()`**: 在 Playwright 測試程式碼中，可以在關鍵步驟前加入 `await page.pause()`，讓測試暫停並打開瀏覽器，方便手動檢查頁面狀態。
*   **增加 `console.log()`**: 在測試程式碼中加入 `console.log()` 輸出變數值或執行流程，幫助追蹤問題。

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

## 部署偵錯指南 (Deployment Debugging Guide)

在 GCP 上部署應用程式時，可能會遇到各種問題。以下是常見問題及其解決方案的總結：

### 1. 80 埠被佔用 (`address already in use`)

*   **現象**：執行 `sudo docker compose up -d --build` 時，Nginx 容器因 80 埠被佔用而無法啟動。
*   **原因**：GCP VM 上預先安裝的 Nginx 或其他服務佔用了 80 埠。
*   **解決方案**：停止並禁用主機上的 Nginx 服務。
    ```bash
    sudo systemctl stop nginx
    sudo systemctl disable nginx
    ```

### 2. 網站無法訪問 / `/swagger` 500 錯誤

*   **現象**：瀏覽器無法訪問網站，或 `/swagger` 頁面顯示 `500 Internal Server Error`。
*   **檢查步驟**：
    1.  **GCP 防火牆**：確認 GCP 防火牆規則允許來自 `0.0.0.0/0` 的 TCP 80 埠入站流量。
    2.  **Nginx 容器日誌**：檢查 Nginx 容器日誌 (`sudo docker compose logs nginx`)，尋找 `502 Bad Gateway` 或 `connect() failed` 等錯誤。
    3.  **後端容器日誌**：檢查後端容器日誌 (`sudo docker compose logs backend`)，尋找應用程式啟動或運行時的錯誤。
    4.  **Nginx 配置**：確認 `nginx/nginx.conf` 中的代理規則正確，特別是 `/api/`、`/swagger/` 和 `/redoc/` 等路徑。
        *   **常見問題**：`location /` 區塊過於通用，導致與後端路徑衝突，產生重定向循環。
        *   **解決方案**：將更具體的代理規則 (如 `/swagger/`, `/redoc/`, `/api/`, `/admin/`) 放在 `location /` 之前。
    5.  **Django `settings.py`**：
        *   **`CORS_ALLOWED_ORIGINS`**：確保 `CORS_ALLOWED_ORIGINS` 包含您 GCP VM 的外部 IP 位址。建議從環境變數動態載入。
        *   **`ALLOWED_HOSTS`**：確保 `ALLOWED_HOSTS` 包含 `*` 或您 GCP VM 的外部 IP 位址。
        *   **`DEBUG` 模式**：在偵錯時，可以暫時將 `DEBUG = True` 設定在 `settings.py` 中，以獲取詳細的錯誤追溯頁面。

### 3. 首頁 `403 Forbidden` 或空白頁面

*   **現象**：訪問首頁時顯示 `403 Forbidden` 或空白頁面。
*   **檢查步驟**：
    1.  **Node.js 和 npm 安裝**：確認 GCP VM 上已安裝 Node.js 和 npm。
        *   **解決方案**：如果未安裝，請安裝 (`sudo apt install nodejs npm`)。
    2.  **Node.js 版本**：確認 Node.js 版本符合前端框架 (如 Vite) 的要求。
        *   **解決方案**：如果版本過舊，請升級 Node.js。
    3.  **前端建置**：確認前端專案已成功建置。
        *   **解決方案**：進入 `frontend` 目錄，執行 `npm install` 和 `npm run build`。
    4.  **權限問題**：建置前端時可能遇到 `EACCES: permission denied` 錯誤。
        *   **解決方案**：修正 `frontend` 目錄的權限 (`sudo chown -R <your_user>:<your_user> /home/<your_user>/med-appointment/frontend`)。
    5.  **Docker Compose 重建**：每次修改前端程式碼或 Nginx 配置後，務必執行 `sudo docker compose down` 和 `sudo docker compose up -d --build` 來重建並重啟服務。

---

## API 文件 (API Documentation)

當應用程式啟動後，您可以透過 `http://localhost/swagger/` 或 `http://localhost/redoc/` 存取 API 文件。
