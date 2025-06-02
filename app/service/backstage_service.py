from app.util.db import get_db

''' 書籍頁 '''
def get_book_list(search_keyword, page, items_per_page=10):
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


def get_total_pages(search_keyword, items_per_page=10):
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
            'SELECT quantity FROM purchase_cart WHERE user_id = ? AND isbn = ?',
            (user_id, isbn)
        ).fetchone()
        
        if existing:
            # 如果已存在，更新數量
            new_quantity = existing['quantity'] + quantity
            db.execute(
                'UPDATE purchase_cart SET quantity = ? WHERE user_id = ? AND isbn = ?',
                (new_quantity, user_id, isbn)
            )
            print(f"書籍 ISBN: {isbn} 已存在，數量更新為 {new_quantity}")
        else:
            # 否則插入新項目
            db.execute(
                'INSERT INTO purchase_cart (user_id, isbn, quantity) VALUES (?, ?, ?)',
                (user_id, isbn, quantity)
            )
            print(f"書籍 ISBN: {isbn}, 數量: {quantity} 已加入訂單購物車")

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"加入訂單購物車時發生錯誤: {e}")
        raise e


''' 購物車頁 '''
def get_cart_content(user_id):
    db = get_db()

    # 使用 JOIN 一次取得 isbn、quantity 與書名 title
    cart_content = db.execute('''
        SELECT c.isbn, c.quantity, b.title
        FROM purchase_cart c
        JOIN books b ON c.isbn = b.isbn
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()

    if not cart_content:
        return []
    else:
        return [dict(row) for row in cart_content]


def send_purchase_order(user_id):
    db = get_db()

    try:
        # 先檢查購物車是否有內容
        existing = db.execute(
            'SELECT COUNT(*) FROM purchase_cart WHERE user_id = ?',
            (user_id,)
        ).fetchone()

        if existing[0] > 0:
            # 如果購物車有商品，則獲取isbn、quantity
            book_list = db.execute(
                'SELECT isbn, quantity FROM purchase_cart WHERE user_id = ?',
                (user_id,)
            ).fetchall()

            # 清空購物車
            db.execute(
                'DELETE FROM purchase_cart WHERE user_id = ?',
                (user_id,)
            )

            # 建立訂單紀錄(未實現)

            db.commit()

            # 返回成功訊息
            print(f"訂單送出成功")
            return True
        else:
            # 如果購物車沒有商品，則返回錯誤訊息
            print(f"購物車沒有商品")
            return False

    except Exception as e:
        print(f"訂單送出失敗: {e}")
        db.rollback()
        return False

def remove_from_purchase_cart(user_id, isbn):
    db = get_db()

    try:
        print(f"移除書籍 user_id: {user_id}, ISBN: {isbn}")
        db.execute(
            'DELETE FROM purchase_cart WHERE user_id = ? AND ISBN = ?',
            (user_id, isbn)
        )
        db.commit()

        # 返回成功訊息
        return True
    except Exception as e:
        print(f"商品移除購物車失敗: {e}")
        db.rollback()
        return False



''' 簽收 ''' # 簽收需要更新庫存、檢查補貨清單
