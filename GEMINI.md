# Side Project 開發計畫：醫療預約系統

本文件旨在為醫療預約系統的 Side Project 提供一個完整的開發流程與藍圖。專案旨在展示 Django、Vue.js 與 MySQL 的技術能力，並嚴格遵循測試驅動開發（TDD）方法論。

## 1. 專案目標

- **技術展示**: 專為應徵職缺而設計，專注於展示 Python (Django)、MySQL 及前端框架 (Vue.js) 的實作能力。
- **TDD 實踐**: 全程採用 TDD 開發，確保程式碼品質、可維護性與穩定性。
- **完整產品週期**: 從系統設計、開發、測試到部署，模擬一個完整的產品開發流程。

## 2. 核心技術棧

- **後端**: Django, Django REST Framework
- **前端**: Vue.js, Vue Router, Pinia (或 Vuex)
- **資料庫**: MySQL
- **測試**:
    - **後端**: PyTest, Django's `TestCase`
    - **前端**: Vitest, Vue Testing Library
- **API 文件**: drf-yasg (Swagger UI)
- **版本控制**: Git (Gitflow)
- **部署**: AWS (EC2 + RDS)

## 3. 開發方法論：測試驅動開發 (TDD)

我們將遵循 "Red-Green-Refactor" 的 TDD 循環：

1.  **Red (紅燈)**: 針對一個新功能，先撰寫一個會失敗的測試案例。這個測試定義了功能的期望行為。
2.  **Green (綠燈)**: 撰寫最精簡的程式碼，剛好能讓測試通過即可。
3.  **Refactor (重構)**: 在測試保護下，優化程式碼的結構、可讀性與效能，同時確保所有測試依然通過。

此方法將應用於後端 API 和前端元件的開發。

## 4. 開發流程與階段

---

### **Phase 0: 環境建置與專案初始化**

1.  **環境準備**:
    - 安裝 Python, Node.js, MySQL Server。
    - 建立 Python 虛擬環境 (`python -m venv venv`)。
2.  **後端初始化**:
    - 安裝 Django, Django REST Framework, `mysqlclient`, `pytest-django`。
    - 執行 `django-admin startproject med_appointment`。
    - 建立 `api` app (`python manage.py startapp api`)。
    - 在 `settings.py` 中設定 MySQL 資料庫連線。
    - 執行 `python manage.py migrate` 確認資料庫連線成功。
3.  **前端初始化**:
    - 使用 `npm create vue@latest` 建立 Vue.js 專案。
    - 選擇包含 `Vue Router`, `Pinia`, `Vitest` 的配置。
    - 安裝 `axios` 用於 API 請求。
4.  **Git 初始化**:
    - `git init`
    - 建立 `main` 與 `develop` 分支，遵循 Gitflow 規範。

---

### **Phase 1: 後端 API 開發 (TDD)**

依據下方的功能列表與 ERD，針對每一個 API Endpoint 進行 TDD 開發。

**範例：開發使用者註冊 API (`/api/register/`)**

1.  **Red**: 在 `api/tests.py` 中撰寫一個測試，模擬 POST 請求到 `/api/register/`，並斷言 (assert) 回應狀態碼為 201、資料庫中多了一位使用者。此時執行測試應為失敗。
2.  **Green**:
    - 在 `api/models.py` 建立 `Patient` 模型。
    - 執行 `makemigrations` 和 `migrate`。
    - 在 `api/serializers.py` 建立 `PatientSerializer`。
    - 在 `api/views.py` 建立一個 `APIView`，處理 POST 請求，驗證資料並儲存使用者。
    - 在 `api/urls.py` 設定路由。
    - 執行測試，直到通過。
3.  **Refactor**: 檢視 View 和 Serializer 的程式碼，是否有重複或可優化之處。

**需開發的 API Endpoints:**

- **使用者/病患**: `POST /api/register/`, `POST /api/login/`, `GET /api/me/`, `PUT /api/me/`
- **醫師**: `GET /api/doctors/`, `GET /api/doctors/{id}/`
- **時段**: `GET /api/schedules/?doctor_id=&date=`
- **預約**: `POST /api/appointments/`, `GET /api/appointments/`, `PATCH /api/appointments/{id}/cancel/`

---

### **Phase 2: 前端介面開發 (TDD)**

**範例：開發註冊頁面**

1.  **Red**: 撰寫一個測試，驗證註冊頁面元件 (`Register.vue`) 是否成功渲染出 "註冊" 標題、以及包含 email、密碼等輸入框。執行測試應為失敗。
2.  **Green**: 在 `Register.vue` 中加入必要的 HTML 結構讓測試通過。
3.  **Red**: 撰寫下一個測試，模擬使用者在輸入框填寫資料並點擊送出按鈕後，會呼叫 `axios.post` 方法。
4.  **Green**: 在元件的 `<script setup>` 中撰寫處理表單提交的函式，並呼叫 API。
5.  **Refactor**: 整理程式碼，將 API 呼叫邏輯抽離成可重用的 `apiService.js`。

**需開發的前端頁面/元件:**

- 註冊/登入頁面
- 個人資訊頁面 (含歷史預約)
- 醫師列表頁面
- 醫師詳情與可預約時段頁面
- 預約確認頁面

---

### **Phase 3: 整合與端對端 (E2E) 測試**

1.  **前後端串接**: 將前端開發好的頁面與後端 API 進行完整串接。
2.  **CORS 設定**: 在 Django 中設定 `django-cors-headers`，允許前端的來源 (e.g., `http://localhost:5173`) 存取 API。
3.  **E2E 測試**: (可選，但加分) 使用 Cypress 或 Playwright 撰寫測試腳本，模擬完整的使用者流程（例如：從註冊、登入、選擇醫師、到成功預約）。

---

### **Phase 4: API 文件與部署**

1.  **API 文件**:
    - 安裝 `drf-yasg`。
    - 在專案的 `urls.py` 中加入 Swagger/ReDoc 的路由。
    - 確保 API 文件能正確呈現所有 Endpoints。
2.  **部署 (AWS)**:
    - **資料庫**: 建立一個 AWS RDS for MySQL 實例。將 Django `settings.py` 中的資料庫設定指向 RDS。
    - **後端**:
        - 將 Django 專案打包成 Docker Image。
        - 部署至 AWS EC2，使用 Gunicorn + Nginx 提供服務。
    - **前端**:
        - 執行 `npm run build`。
        - 將 `dist` 目錄下的靜態檔案部署到 S3 或直接由 Nginx 提供。
    - **CI/CD**: (可選) 設定 GitHub Actions，當 `main` 分支有更新時，自動執行測試、打包並部署到 AWS。

---

## 附錄 A: 功能列表 (Feature List)

### 使用者 / 病患相關
1.  **註冊 / 登入**: Email、姓名、生日、手機、密碼。登入使用 JWT。
2.  **個人資訊管理**: 更新個人資料、查詢歷史預約紀錄。

### 醫師相關
1.  **醫師基本資料管理**: 姓名、專科、門診時段。
2.  **醫師時段設定**: 定義可掛號時間。

### 預約相關
1.  **建立預約**: 病患選擇醫師、日期、時段。成功後鎖定該時段。
2.  **查詢預約**: 病患查詢自己的預約；醫師查詢當日預約名單。
3.  **取消預約**: 病患可取消，系統自動釋放時段。

---

## 附錄 B: ERD 設計 (簡化版)

```
[Patient]
- patient_id (PK)
- name
- email (unique)
- phone
- password_hash
- birthday
- created_at

[Doctor]
- doctor_id (PK)
- name
- specialty
- department
- created_at

[Schedule]
- schedule_id (PK)
- doctor_id (FK to Doctor)
- date
- start_time
- end_time
- is_available (boolean, default: true)

[Appointment]
- appointment_id (PK)
- patient_id (FK to Patient)
- schedule_id (FK to Schedule)
- status (e.g., 'booked', 'cancelled', 'completed')
- created_at
```

---

## 附錄 C: 面試 Demo 流程

1.  **用 Swagger 打開 API Docs**: 展示所有 Endpoint。
2.  **註冊 / 登入**: Demo 病患註冊及登入流程，取得 JWT Token。
3.  **查詢醫師清單**: `GET /api/doctors/`。
4.  **查詢醫師可預約時段**: `GET /api/schedules/?doctor_id=1&date=...`。
5.  **建立預約**: `POST /api/appointments/`，並展示資料庫中的變化。
6.  **查詢與取消預約**: Demo `GET` 和 `PATCH` appointments 的功能。
