'''
import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """獲取資料庫連接"""
    if 'db' not in g:
        g.db = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database=current_app.config['DATABASE'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
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
        with db.cursor() as cursor:
            cursor.execute(f.read().decode('utf8'))
        db.commit()

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

'''