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
git push origin main
```

> ⛔ **請勿跳過 commit 步驟直接 push**

---

## ✏️ Commit 命名建議

請用簡潔明確的方式命名 commit 訊息，例如：

* `add login feature`
* `fix bug in signup logic`
* `update ER diagram`
* `refactor query structure`
* `docs: update README.md`

---
