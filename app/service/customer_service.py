from app.util.db import get_db

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

def get_customer_profile_by_user_id(user_id):
    """根據用戶ID獲取完整的顧客資料（包含用戶基本資料和顧客特定資料）"""
    db = get_db()
    # 連接 users 表和 customer 表獲取完整資訊
    profile = db.execute(
        'SELECT u.user_id, u.name, u.created_at, c.email, c.address, c.balance '
        'FROM users u '
        'LEFT JOIN customer c ON u.user_id = c.user_id '
        'WHERE u.user_id = ? AND u.user_type = "customer"',
        (user_id,)
    ).fetchone()
    return profile
