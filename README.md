# 醫療預約系統 Side Project

這是一個用於展示 Django、Vue.js 與 MySQL 技術能力的 Side Project，嚴格遵循測試驅動開發（TDD）方法論，並模擬一個完整的產品開發流程。

## 專案目標

-   **技術展示**: 專為應徵職缺而設計，專注於展示 Python (Django)、MySQL 及前端框架 (Vue.js) 的實作能力。
-   **TDD 實踐**: 全程採用 TDD 開發，確保程式碼品質、可維護性與穩定性。
-   **完整產品週期**: 從系統設計、開發、測試到部署，模擬一個完整的產品開發流程。

## 核心技術棧

-   **後端**: Django, Django REST Framework
-   **前端**: Vue.js, Vue Router, Pinia
-   **資料庫**: MySQL
-   **測試**:
    -   **後端單元/整合測試**: PyTest, Django's `TestCase`
    -   **前端單元/元件測試**: Vitest, Vue Testing Library
    -   **端對端 (E2E) 測試**: Playwright, `npm-run-all`, `wait-on`
-   **API 文件**: drf-yasg (Swagger UI)
-   **版本控制**: Git (遵循 Gitflow 工作流)

## 目前進度

專案已完成核心的後端 API 和前端註冊/登入功能，並建立了強大的測試基礎設施。

### 後端 (Django REST Framework)
-   已實現以下 API 端點：
    -   使用者/病患註冊 (`POST /api/register/`)
    -   使用者登入 (`POST /api/login/`)
    -   使用者個人資訊管理 (`GET /api/me/`, `PUT /api/me/`)
    -   醫師列表與詳情 (`GET /api/doctors/`, `GET /api/doctors/{id}/`)
    -   醫師時段查詢 (`GET /api/schedules/`)
    -   預約建立、查詢與取消 (`POST /api/appointments/`, `GET /api/appointments/`, `PATCH /api/appointments/{id}/cancel/`)
-   所有已實現的 API 端點均有全面的整合測試覆蓋。

### 前端 (Vue.js)
-   已完成註冊和登入頁面的開發。
-   相關元件（如 `Register.vue`, `Login.vue`）均有單元測試覆蓋。

### 測試基礎設施
-   **TDD 實踐**: 專案嚴格遵循 Red-Green-Refactor 的 TDD 循環進行開發。
-   **自動化 E2E 測試**: 建立了自動化 E2E 測試流程，能夠一鍵啟動前後端伺服器、執行測試並自動關閉。

## 如何開始 (Getting Started)

### 1. 環境準備
-   安裝 Python (建議 3.9+), Node.js (建議 18+), MySQL Server。
-   建立 Python 虛擬環境並安裝依賴：
    ```bash
    python -m venv venv
    source venv/bin/activate # macOS/Linux
    # venv\Scripts\activate # Windows
    pip install -r requirements.txt # 假設您有 requirements.txt
    ```
-   進入 `frontend` 目錄安裝前端依賴：
    ```bash
    cd frontend
    npm install
    ```

### 2. 啟動開發伺服器
-   **後端**: 在專案根目錄下執行：
    ```bash
    python manage.py runserver
    ```
-   **前端**: 在 `frontend` 目錄下執行：
    ```bash
    npm run dev
    ```
    前端伺服器預設會在 `http://localhost:5173` 啟動。

### 3. 執行測試

#### 後端測試
在專案根目錄下，確保虛擬環境已啟動，執行：
```bash
pytest
```
或直接使用虛擬環境中的 pytest：
```bash
./venv/bin/pytest
```

#### 前端單元/元件測試
在 `frontend` 目錄下執行：
```bash
npm test
```
此指令會執行 `vitest run`，測試完成後自動結束。若需監聽模式，可執行 `npx vitest`。

#### 端對端 (E2E) 測試
在 `frontend` 目錄下執行：
```bash
npm run test:e2e
```
此指令會自動啟動前後端伺服器，等待其就緒，執行 Playwright 測試，並在測試完成後自動關閉伺服器。

## 專案結構 (Project Structure)

```
.
├── api/                # Django 後端 API 應用
├── frontend/           # Vue.js 前端應用
├── med_appointment/    # Django 專案設定
├── manage.py           # Django 管理命令
├── pytest.ini          # Pytest 設定
├── README.md           # 專案說明 (此文件)
└── venv/               # Python 虛擬環境
```

## 附錄 (Appendices)

-   **功能列表**: 詳細列出所有已規劃和待開發的功能。
-   **ERD 設計**: 簡化版的實體關係圖。
-   **Demo 流程**: 演示專案核心功能的步驟。