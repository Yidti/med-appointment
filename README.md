# 醫療預約系統 Side Project

這是一個用於展示 Django、Vue.js 與 MySQL 技術能力的 Side Project，嚴格遵循測試驅動開發（TDD）方法論，並模擬一個完整的產品開發流程。

## 核心技術棧

-   **後端**: Django, Django REST Framework
-   **前端**: Vue.js, Vue Router, Pinia
-   **資料庫**: MySQL
-   **測試**: PyTest, Vitest, Playwright
-   **API 文件**: drf-yasg (Swagger UI)

---

## 開發環境設定 (Local Development Setup)

請依照以下步驟在您的本機環境中設定並執行此專案。

### 1. 環境準備

-   確認您已安裝 **Python** (建議 3.9+)
-   確認您已安裝 **Node.js** (建議 18+)
-   **資料庫**: 本專案使用 **MySQL**。請確認您已安裝並啟動 MySQL Server，並在 `med_appointment/settings.py` 中設定正確的連線資訊 (使用者、密碼等)。

### 2. 後端設定

從專案根目錄開始：

```bash
# 1. 建立並啟動 Python 虛擬環境
python -m venv venv
source venv/bin/activate # macOS/Linux
# .\venv\Scripts\activate # Windows

# 2. 安裝 Python 依賴套件
pip install -r requirements.txt

# 3. 執行資料庫遷移
python manage.py migrate

# 4. 建立後台管理員帳號
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

```bash
# 確認您仍在 frontend 目錄下
cd frontend

# 執行啟動指令
npm run start
```

-   後端 API 將運行在 `http://localhost:8000`
-   前端網站將運行在 `http://localhost:5173`

### 5. (重要) 新增範例資料

為了讓系統能夠正常操作，您需要先新增一些醫師和時段資料。

1.  **開啟後台網頁**：瀏覽器開啟 [http://localhost:8000/admin/](http://localhost:8000/admin/)
2.  **登入**：使用您在步驟 2.4 中建立的**管理員帳號密碼**登入。
3.  **新增資料**：
    -   點擊 `Doctors` 並新增幾位醫師。
    -   點擊 `Schedules` 並為醫師新增一些可預約的時段。

完成後，您就可以開啟前端網站 `http://localhost:5173`，註冊一個普通使用者帳號，並開始進行預約操作。

**快速提示**: 您也可以在專案根目錄下，執行 `venv/bin/python manage.py seed_test_doctor` 指令，來快速新增一位名為 "E2E Test Doctor" 的醫師及他的未來班表。

---

## 測試

#### 後端測試

```bash
# 確保虛擬環境已啟動
pytest
```

#### 前端單元/元件測試

```bash
cd frontend
npm test
```

#### 端對端 (E2E) 測試

```bash
cd frontend
npm run test:e2e
```

---

## API 文件 (API Documentation)

本專案使用 `drf-yasg` 自動產生 API 文件。

當後端伺服器啟動後，您可以透過以下網址存取互動式的 API 文件：

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)