import os
import sys
import sqlite3

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 現在可以導入專案模組
from app import create_app
from app.util.db import get_db

def insert_fake_data():
    app = create_app()
    with app.app_context():
        db = get_db()
        with open('app/data/insert_fake_data.sql', 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()
        print("假資料已成功插入資料庫！")

if __name__ == "__main__":
    insert_fake_data()