from app.util.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_id(user_id):
    """根據 ID 獲取用戶"""
    db = get_db()
    user = db.execute(
        'SELECT user_id, name, password, user_type, created_at FROM users WHERE user_id = ?',
        (user_id,)
    ).fetchone()
    return user

def get_user_by_username(username):
    """根據用戶名獲取用戶"""
    db = get_db()
    user = db.execute(
        'SELECT user_id, name, password, user_type, created_at FROM users WHERE name = ?',
        (username,)
    ).fetchone()
    return user

def create_user(username, password, user_type):
    """創建新用戶"""
    db = get_db()
    db.execute(
        'INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
        (username, generate_password_hash(password), user_type)
    )

    if user_type == 'customer':
        db.execute(
            'INSERT INTO customer (user_id) VALUES (?)',
            (user_id,)
        )
    elif user_type == 'staff':
        db.execute(
            'INSERT INTO staff (user_id) VALUES (?)',
            (user_id,)
        )
    db.commit()
    #return db.execute('SELECT last_insert_rowid()').fetchone()[0]
    return user_id

def verify_password(user, password):
    """驗證用戶密碼"""
    if user and check_password_hash(user['password'], password):
        return True
    return False 