
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

