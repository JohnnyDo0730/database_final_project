from app.util.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_id(user_id):
    """根據 ID 獲取用戶"""
    db = get_db()
    user = db.execute(
        'SELECT user_id, name, user_type, created_at FROM users WHERE user_id = ?',
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

def create_user(username, password, user_type, email=None, address=None):
    """創建新用戶"""
    db = get_db()
    # 開始事務
    db.execute('BEGIN')
    try:
        # 插入用戶基本信息
        db.execute(
            'INSERT INTO users (name, password, user_type) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), user_type)
        )
        user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # 根據用戶類型插入額外信息
        if user_type == 'customer':
            db.execute(
                'INSERT INTO customer (user_id, email, address) VALUES (?, ?, ?)',
                (user_id, email, address)
            )
        elif user_type == 'staff':
            db.execute(
                'INSERT INTO staff (user_id) VALUES (?)',
                (user_id,)
            )
        
        # 提交事務
        db.commit()
        return user_id
    except Exception as e:
        # 發生錯誤時回滾
        db.execute('ROLLBACK')
        raise e

def verify_password(user, password):
    """驗證用戶密碼"""
    if user and check_password_hash(user['password'], password):
        return True
    return False 

def get_customer_profile_by_username(username):
    """根據用戶名獲取完整的顧客資料（包含用戶基本資料和顧客特定資料）"""
    db = get_db()
    # 連接 users 表和 customer 表獲取完整資訊
    profile = db.execute(
        'SELECT u.user_id, u.name, u.created_at, c.email, c.address, c.balance '
        'FROM users u '
        'LEFT JOIN customer c ON u.user_id = c.user_id '
        'WHERE u.name = ? AND u.user_type = "customer"',
        (username,)
    ).fetchone()
    return profile