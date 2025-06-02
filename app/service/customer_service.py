from app.util.db import get_db

''' 書籍頁 '''
def get_book_list(search_keyword, page, items_per_page=12):
    db = get_db()
    books = db.execute(
        'SELECT * FROM books WHERE title LIKE ? LIMIT ? OFFSET ?;',
        ('%' + search_keyword + '%', items_per_page, (page - 1) * items_per_page)
    ).fetchall()

    if not books: # 如果 books 為空，則返回空列表
        return []
    else: # 如果 books 不為空，則將 books 轉換為字典列表
        books_list = [dict(row) for row in books]
        return books_list


def get_total_pages(search_keyword, items_per_page=12):
    db = get_db()
    total_pages = db.execute(
        'SELECT COUNT(*) FROM books WHERE title LIKE ?',
        ('%' + search_keyword + '%',)
    ).fetchone()[0]

    if total_pages % items_per_page == 0:
        return total_pages//items_per_page
    else:
        return total_pages//items_per_page + 1

def add_to_cart(user_id, isbn, quantity):
    db = get_db()

    try:
        # 先檢查是否已有這本書在購物車
        existing = db.execute(
            'SELECT quantity FROM cart WHERE user_id = ? AND isbn = ?',
            (user_id, isbn)
        ).fetchone()
        
        if existing:
            # 如果已存在，更新數量
            new_quantity = existing['quantity'] + quantity
            db.execute(
                'UPDATE cart SET quantity = ? WHERE user_id = ? AND isbn = ?',
                (new_quantity, user_id, isbn)
            )
            print(f"書籍 ISBN: {isbn} 已存在，數量更新為 {new_quantity}")
        else:
            # 否則插入新項目
            db.execute(
                'INSERT INTO cart (user_id, isbn, quantity) VALUES (?, ?, ?)',
                (user_id, isbn, quantity)
            )
            print(f"書籍 ISBN: {isbn}, 數量: {quantity} 已加入購物車")

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"加入購物車時發生錯誤: {e}")
        raise e





''' 客戶資訊頁 '''
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
