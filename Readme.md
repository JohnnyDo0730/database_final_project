# Database Final Project

這是我們的資料庫期末專案，包含初始化環境步驟、Git 使用流程與命名規則等說明。

## 📦 專案初始化

### 1. 初次 Push（首次建立 GitHub 倉庫後）

```bash
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/JohnnyDo0730/database_final_project.git
git push -u origin main
```

---

## 🐍 Python 環境管理（使用 pipenv）

### 初始化虛擬環境

```bash
pipenv install
```

### 進入虛擬環境

```bash
pipenv shell
```

### 安裝套件並自動記錄到 Pipfile

```bash
pipenv install package_name
```

### 退出虛擬環境

```bash
exit
```

### 匯出套件清單

```bash
pipenv requirements > requirements.txt
```

---

## 🔃 Git 常用操作流程

### 獲取遠端更新（**每次開始作業前**）

```bash
git pull origin main
```

### 新增或更新檔案後，將變更提交與上傳

```bash
git add .
git commit -m "簡要說明本次變更"
git push origin branch_name
```

> ⛔ **請勿跳過 commit 步驟直接 push**

---
🌿 分支命名原則
請依據用途建立分支，建議格式如下：

類型	命名範例	說明
功能	feature/login-system	新增功能
修復	fix/login-bug	修正錯誤
重構	refactor/db-structure	調整架構或重構
文件	docs/update-readme	修改說明文件
測試	test/db-connection	測試功能相關

建立新分支範例：

```bash
git checkout -b feature/some-feature-name
```

💡 一次完整工作流程範例
從 main 更新並建立新功能分支

```bash
git checkout main
git pull origin main
git checkout -b feature/login-api
進行開發與測試...
```

提交與推送分支

```bash
git add .
git commit -m "add login API and validation"
git checkout -b feature/login-api
git push origin feature/login-api
進 GitHub 建立 Pull Request，指向 main
```
由自己或組員審查並合併

合併後可刪除該分支
```bash
git branch -d feature/login-api          # 本地刪除
git push origin --delete feature/login-api  # 遠端刪除
```
---

## ✏️ Commit 命名建議

請用簡潔明確的方式命名 commit 訊息，例如：

* `add login feature`
* `fix bug in signup logic`
* `update ER diagram`
* `refactor query structure`
* `docs: update README.md`

---
