# Database Final Project

這是我們的資料庫期末專案，包含初始化環境步驟、Git 使用流程與命名規則等說明。

## 📋 專案架構

```
project/
│
├── app/                        # 應用程式主目錄
│   ├── __init__.py             # 應用程式初始化
│   ├── data/                   # 資料相關檔案
│   ├── modules/                # 功能模組
│   ├── route/                  # 路由控制
│   │   ├── __init__.py         # 路由初始化
│   │   └── main_routes.py      # 主要頁面路由
│   ├── service/                # 服務層
│   │   └── __init__.py         # 服務層初始化
│   ├── static/                 # 靜態檔案
│   │   ├── css/                # CSS 樣式表
│   │   └── js/                 # JavaScript 檔案
│   ├── templates/              # HTML 模板
│   │   ├── login.html          # 登入頁面
│   │   ├── customer_base.html  # 客戶端基本模板
│   │   └── backstage_base.html # 後台基本模板
│   └── util/                   # 工具函數
│       └── db.py               # 資料庫連接工具
│
├── run.py                      # 應用程式入口點
├── Pipfile                     # 依賴管理
├── Pipfile.lock                # 依賴版本鎖定
└── Readme.md                   # 專案說明文件
```

## 🚀 快速開始

### 補充說明
- 私人檔案(沒有要上傳的)，請放在project_root/self裡面
- 其他不想上傳的檔案可在.gitignore中新增路徑來自動忽略

### 環境需求

- Python 3.12
- pipenv (用於管理虛擬環境和依賴)

### 安裝步驟

1. 複製專案到本地

```bash
git init
git remote add origin https://github.com/JohnnyDo0730/Image-Inpainting.git
git pull origin main
```

2. 安裝依賴

```bash
pip install pipenv
pipenv install
```

3. 啟動虛擬環境

```bash
pipenv shell
```

4. 啟動應用程式（強制使用當前虛擬環境執行）

```bash
pipenv run python run.py
```

應用程式將在 http://localhost:5000 啟動

5. 退出虛擬環境

```bash
exit
```

---

## 🔃 Git 常用操作流程

### 獲取遠端更新（**每次開始作業前**）

```bash
git pull origin main
```

### 新增或更新檔案後，將變更提交與上傳

```bash
git checkout -b feature/some-feature-name
git add .
git commit -m "簡要說明本次變更"
git push origin feature/some-feature-name
```

---
🌿 分支命名原則
請依據用途建立分支，建議格式如下：

| 類型 | 命名範例                    | 說明      |
| -- | ----------------------- | ------- |
| 功能 | `feature/login-system`  | 新增功能    |
| 修復 | `fix/login-bug`         | 修正錯誤    |
| 重構 | `refactor/db-structure` | 調整架構或重構 |
| 文件 | `docs/update-readme`    | 修改說明文件  |
| 測試 | `test/db-connection`    | 測試功能相關  |

---

 ✏️ Commit 命名建議

請用簡潔明確的方式命名 commit 訊息，例如：

* `add login feature`
* `fix bug in signup logic`
* `update ER diagram`
* `refactor query structure`
* `docs: update README.md`

---

## 🔧 技術架構

- **前端**：HTML、CSS、JavaScript
- **後端**：Python、Flask
- **資料庫**：SQLite (內建於 Python 標準庫)
- **環境管理**：pipenv

## 📝 開發注意事項

1. 目前專案處於基本架構階段，已實作基本資料庫連接
2. 資料庫檔案會自動在 `instance` 目錄下創建
3. 初始化資料庫可使用以下命令(只有第一次需要執行)：
   ```bash
   flask init-db
   ```
4. 開發新功能時，請遵循以下步驟：
   - 創建新分支
   - 在適當目錄下添加功能模組
   - 更新相關路由
   - 提交變更並發起 Pull Request
