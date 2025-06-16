
import sqlite3
import click
import os
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """獲取 SQLite 資料庫連接"""
    if 'db' not in g:
        # 確保資料庫目錄存在
        os.makedirs(os.path.dirname(current_app.config['DATABASE']), exist_ok=True)
        
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """關閉資料庫連接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """初始化資料庫"""
    db = get_db()
    with current_app.open_resource('data/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """清除現有資料並創建新表"""
    init_db()
    click.echo('資料庫初始化完成')

def init_app(app):
    """在應用中註冊資料庫函數"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) 

    with app.app_context():
        # 初始化資料表
        init_db()

        # 執行 app\data\real_books_schema.sql的SQL語句
        with current_app.open_resource('data/real_books_schema.sql') as f:
            db = get_db()
            db.executescript(f.read().decode('utf8'))
            db.commit()

        # 執行 app\data\fake_user_schema.sql的SQL語句
        with current_app.open_resource('data/fake_user_schema.sql') as f:
            db = get_db()
            db.executescript(f.read().decode('utf8'))
            db.commit()

        # 刪除 app\data\fake_data_schema.sql 舊語句
        fake_data_schema_path = os.path.join(current_app.root_path, 'data', 'fake_data_schema.sql')
        if os.path.exists(fake_data_schema_path):
            os.remove(fake_data_schema_path)
            print(f"已刪除舊的 fake_data_schema.sql 檔案")

        # 執行app\data\generate_fake_data_schema.py產生新的資料(符合當日)之SQL語句
        import subprocess
        subprocess.run(['pipenv', 'run', 'python', 'app/data/generate_fake_data_schema.py'], check=True)

        # 執行 app\data\fake_data_schema.sql的SQL語句
        with current_app.open_resource('data/fake_data_schema.sql') as f:
            db = get_db()
            db.executescript(f.read().decode('utf8'))
            db.commit()

        # 手動更新每本書的庫存
        from app.service.customer_service import update_book_restock
        ## 對每個書執行一次檢查 (isbn list，以換行分隔: app\data\isbn_list.txt)
        with open('app/data/isbn_list.txt', 'r') as f:
            isbn_list = f.read().splitlines()
            for isbn in isbn_list:
                update_book_restock(isbn)