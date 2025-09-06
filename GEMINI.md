# 當前狀態 (Current Status)

- **[✓] Phase 0: 環境建置與專案初始化** - 已完成
- **[✓] Phase 1: 後端 API 開發 (TDD)** - 已完成
- **[✓] Phase 2: 前端介面開發 (TDD)** - 已完成
    - **[✓]** 註冊/登入頁面
    - **[✓]** 醫師列表頁面
    - **[✓]** 醫師詳情與可預約時段頁面
    - **[✓]** 個人資訊頁面 (含歷史預約)
    - **[✓]** 預約確認頁面
- **[✓] Phase 3: 整合與端對端 (E2E) 測試** - 已完成
    - **[✓]** 註冊流程
    - **[✓]** 登入與預約主流程
- **[ ] Phase 4: API 文件與部署** - 未開始

---

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
- **版本控制**: Git (遵循 Gitflow 工作流)
    - **主要分支**:
        - `main`: 用於存放穩定、可部署的正式版本。**嚴禁直接推送 (push) 到此分支。** 所有對 `main` 的變更都必須透過 Pull Request (PR) 流程來完成。
            - **Pull Request (PR) 流程**:
                1.  **完成開發**: 確保所有相關功能都在 `develop` 分支開發完成，並已推送到遠端。
                2.  **建立 PR**: 在 Git 平台（如 GitHub）上，從 `develop` 分支向 `main` 分支發起一個新的 Pull Request。
                3.  **描述與審查**: 在 PR 中詳細描述變更內容，並指定至少一位團隊成員進行程式碼審查 (Code Review)。
                4.  **通過自動化測試**: PR 會觸發自動化的測試流程（單元測試、E2E 測試等），必須全部通過。
                5.  **合併**: 在 PR 獲得批准 (Approve) 且所有測試通過後，才能將其合併到 `main` 分支。
        - `develop`: 主要的開發分支，整合所有已完成的功能。我們目前的工作都應該在這個分支上進行。
    - **支援分支**:
        - `feature/<feature-name>`: 開發新功能時，應從 `develop` 分支出來。完成後合併回 `develop`。
        - `hotfix/<fix-name>`: 修復正式版本的緊急 bug 時，從 `master` 分支出來，完成後同時合併回 `master` 和 `develop`。
    - **Commit 流程**:
        - 在完成一個功能或一個階段性任務後，都應建立一個清晰的 commit。
        - Commit message 應遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範 (例如 `feat(api): ...`, `fix(tests): ...`)，以保持歷史紀錄的可讀性。
        - 完成 commit 後，應將 `develop` 分支推送到遠端儲存庫 (git push origin develop)。
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

**執行後端測試**

要執行後端測試，請確保您已啟動 Python 虛擬環境。您可以使用以下指令執行所有測試：

```bash
pytest
```

如果您想在不啟動虛擬環境的情況下執行測試，可以直接使用虛擬環境中的 `pytest` 執行檔：

```bash
./venv/bin/pytest
```

若要針對特定的 app (例如 `api`) 執行測試，可以指定路徑：

```bash
./venv/bin/pytest api/
```

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

**執行前端測試**

要執行前端單元測試，請在 `frontend` 目錄下使用 `npm test`。

根據 `package.json` 的設定，此指令會執行 `vitest run`，這會完整地跑過一次所有測試，然後自動結束。這非常適合在 CI/CD 或推送程式碼前進行最終驗證。

如果您希望在開發過程中，讓測試工具持續監聽檔案變更並自動重跑測試，可以手動執行 `npx vitest` 或在 `package.json` 中建立一個專門的 `watch` 指令。

**啟動開發伺服器**

為了方便開發，我們建立了一個指令來同時啟動後端 Django 伺服器和前端 Vite 伺服器。請在 `frontend` 目錄下執行：

```bash
npm run start
```

這個指令會自動處理兩個伺erv器的啟動，讓您可以直接在 `http://localhost:5173` 上看到應用程式的變化。

---

### **Phase 3: 整合與端對端 (E2E) 測試**

1.  **前後端串接**: 將前端開發好的頁面與後端 API 進行完整串接。
2.  **CORS 設定**: 在 Django 中設定 `django-cors-headers`，允許前端的來源 (e.g., `http://localhost:5173`) 存取 API。
3.  **E2E 測試**: 使用 Playwright 撰寫測試腳本，模擬完整的使用者流程。

**執行 E2E 測試**

我們已經設定了一個自動化的指令來執行 E2E 測試。請在 `frontend` 目錄下執行：

```bash
npm run test:e2e
```

這個指令會執行以下全自動流程：
1.  使用 `npm-run-all` **同時啟動**後端 Django 伺服器和前端 Vite 伺服器。
2.  使用 `wait-on` **等待** `http://localhost:8000` (後端) 和 `http://localhost:5173` (前端) 都準備就緒。
3.  成功等到之後，執行 `playwright test` 開始進行 E2E 測試。
4.  測試結束後，`npm-run-all` 會**自動關閉**先前啟動的兩個伺服器進程，不會留下殭屍進程。

這個設定確保了 E2E 測試在一個乾淨、一致的環境中執行，大幅提升了測試的便利性與可靠性。

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

## 附錄 C: Demo 流程

1.  **用 Swagger 打開 API Docs**: 展示所有 Endpoint。
2.  **註冊 / 登入**: Demo 病患註冊及登入流程，取得 JWT Token。
3.  **查詢醫師清單**: `GET /api/doctors/`。
4.  **查詢醫師可預約時段**: `GET /api/schedules/?doctor_id=1&date=...`。
5.  **建立預約**: `POST /api/appointments/`，並展示資料庫中的變化。
6.  **查詢與取消預約**: Demo `GET` 和 `PATCH` appointments 的功能。

---

## 附錄 D: 開發資料管理

為了在開發過程中方便測試與驗證，我們需要有基礎資料（例如：醫師、門診時段）。本專案使用 Django 內建的 Admin 後台來管理這些核心資料。

操作流程如下：
1.  **建立超級使用者**：執行 `python manage.py createsuperuser` 來建立後台管理員帳號。
2.  **註冊資料模型**：在 `api/admin.py` 中，將需要管理的模型（如 `Doctor`, `Schedule`）註冊到 Admin 站點。
3.  **新增與管理資料**：啟動後端伺服器後，瀏覽 `http://localhost:8000/admin/`，使用超級使用者帳號登入，即可透過圖形化介面新增、修改或刪除資料。�。