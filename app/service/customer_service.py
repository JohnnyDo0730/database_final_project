from app.util.db import get_db
from datetime import datetime, timedelta

''' 通用 '''
def update_book_restock(isbn, need_commit=True):
    db = get_db()
    book_stock = db.execute(
        'SELECT stock FROM books WHERE ISBN = ?',
        (isbn,)
    ).fetchone()

    book_purchasing = db.execute(
        'SELECT SUM(quantity) FROM po_items WHERE isbn = ?',
        (isbn,)
    ).fetchone()
    
    book_required = db.execute(
        'SELECT SUM(quantity) FROM cart WHERE isbn = ?',
        (isbn,)
    ).fetchone()

    if book_required[0] is None:
        book_required = [0]

    isEnough = book_required[0] <= book_stock[0] + book_purchasing[0]
    if not isEnough:
        # 庫存不足，加入補貨清單
        db.execute(
            'INSERT INTO restock (ISBN, quantity) VALUES (?, ?)',
            (isbn, book_required[0] - book_stock[0])
        )
        print(f"書籍 ISBN: {isbn} 庫存不足，已加入補貨清單")
    else:
        # 庫存足夠，檢查是否需要取消補貨
        has_restock = db.execute(
            'SELECT * FROM restock WHERE ISBN = ?',
            (isbn,)
        ).fetchone()

        # 如果為取消預定後庫存足夠，則從補貨清單中刪除
        if has_restock:
            db.execute(
                'DELETE FROM restock WHERE ISBN = ?',
                (isbn,)
            )
            print(f"書籍 ISBN: {isbn} 已取消預定，已從補貨清單中刪除")

    if need_commit:
        db.commit()
    return isEnough


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
        # 檢查是否已有這本書在購物車
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

        # 更新補貨清單
        isEnough = update_book_restock(isbn,need_commit=False)

        db.commit()
        return isEnough

    except Exception as e:
        db.rollback()
        print(f"加入購物車時發生錯誤: {e}")
        raise e

''' 購物車 '''
def get_cart_content(user_id):
    db = get_db()

    # 使用 JOIN 一次取得 isbn、quantity 與書名 title
    cart_content = db.execute('''
        SELECT c.isbn, c.quantity, b.title
        FROM cart c
        JOIN books b ON c.isbn = b.isbn
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()

    if not cart_content:
        return []
    else:
        return [dict(row) for row in cart_content]

def send_order(user_id):
    db = get_db()

    try:
        # 先檢查購物車是否有內容
        existing = db.execute(
            'SELECT COUNT(*) FROM cart WHERE user_id = ?',
            (user_id,)
        ).fetchone()

        if existing[0] > 0: 
            # 找出庫存足夠的項目
            book_list = db.execute('''
                SELECT c.isbn, c.quantity, b.stock, b.price
                FROM cart c 
                JOIN books b ON c.isbn = b.ISBN 
                WHERE c.user_id = ? AND c.quantity <= b.stock
            ''', (user_id,)).fetchall()

            if not book_list:
                return {"success": False, "message": "沒有任何商品庫存足夠，無法送出訂單"}
          
            # 清除已成功下單的項目（用 IN）
            isbn_list = [row['isbn'] for row in book_list]
            db.execute(f'''
                DELETE FROM cart 
                WHERE user_id = ? AND isbn IN ({','.join(['?']*len(isbn_list))})
            ''', (user_id, *isbn_list))

            # 建立訂單紀錄、扣款
            result = add_to_order(user_id, book_list, need_commit=False)

            db.commit()
            return result
        else:
            # 如果購物車沒有商品，則返回錯誤訊息
            print(f"購物車沒有商品")
            return {"success": False, "message": "購物車沒有商品"}

    except Exception as e:
        print(f"訂單送出失敗: {e}")
        db.rollback()
        return {"success": False, "message": "訂單送出失敗"}

def add_to_order(user_id, book_list, need_commit=True):
    db = get_db()

    try:
        # 計算訂單總金額
        total_amount = sum(book['quantity'] * book['price'] for book in book_list)

        # 檢查顧客餘額
        customer_balance = db.execute(
            'SELECT balance FROM customer WHERE user_id = ?',
            (user_id,)
        ).fetchone()

        if customer_balance[0] < total_amount:
            return {"success": False, "message": "餘額不足"}
        
        # 扣除顧客餘額
        db.execute(
            'UPDATE customer SET balance = balance - ? WHERE user_id = ?',
            (total_amount, user_id)
        )

        # 建立訂單紀錄
        db.execute(
            'INSERT INTO orders (user_id, order_date, order_status) VALUES (?, ?, ?)',
            (user_id, datetime.now().strftime('%Y-%m-%d'), '已送達')
        )

        # 取得訂單編號
        order_id = db.execute(
            'SELECT last_insert_rowid()'
        ).fetchone()[0]

        # 處理每本書
        for book in book_list:
            # 建立訂單項目紀錄
            db.execute(
                'INSERT INTO order_items (order_id, isbn, quantity) VALUES (?, ?, ?)',
                (order_id, book['isbn'], book['quantity'])
            )

            # 更新庫存
            db.execute(
                'UPDATE books SET stock = stock - ? WHERE isbn = ?',
                (book['quantity'], book['isbn'])
            )

        if need_commit:
            db.commit()

        print(f"訂單建立成功，訂單編號: {order_id}")
        return {"success": True, "message": "訂單建立成功"}
    except Exception as e:
        db.rollback()
        print(f"建立訂單時發生錯誤: {e}")
        raise e

def remove_from_cart(user_id, isbn):
    db = get_db()

    try:
        print(f"移除書籍 user_id: {user_id}, ISBN: {isbn}")
        db.execute(
            'DELETE FROM cart WHERE user_id = ? AND isbn = ?',
            (user_id, isbn)
        )

        # 更新補貨清單
        isEnough = update_book_restock(isbn,need_commit=False)

        db.commit()

        # 返回成功訊息
        return True
    except Exception as e:
        print(f"商品移除購物車失敗: {e}")
        db.rollback()
        return False


''' 訂單查詢頁 '''
def get_user_orders(user_id):
    """根據用戶ID獲取所有訂單資料"""
    db = get_db()
    try:
        # 獲取該用戶的所有訂單
        orders = db.execute(
            'SELECT order_id, order_date, order_status FROM orders WHERE user_id = ? ORDER BY order_date DESC',
            (user_id,)
        ).fetchall()

        # 將結果轉換為字典列表
        orders_list = []

        for order in orders:
            order_dict = dict(order)

            # 檢查下單日期是否超過7天
            #資料庫中的格式:datetime.now().strftime('%Y-%m-%d'),type:datetime.date
            order_date = datetime.strptime(str(order_dict['order_date']), '%Y-%m-%d')
            print("order_date:",order_date)
            print("datetime.now() - timedelta(days=7):",datetime.now() - timedelta(days=7))
            if order_date < datetime.now() - timedelta(days=7):
                order_dict['order_status'] = '已送達，不接受退貨(超過7天鑑賞期)'
                db.execute(
                    'UPDATE orders SET order_status = ? WHERE order_id = ?',
                    (order_dict['order_status'], order_dict['order_id'])
                )
                db.commit()

            # 獲取該訂單的所有項目
            order_items = db.execute(
                'SELECT oi.ISBN, oi.quantity, b.title, b.price ' 
                'FROM order_items oi '
                'JOIN books b ON oi.ISBN = b.ISBN '
                'WHERE oi.order_id = ?',
                (order_dict['order_id'],)
            ).fetchall()

            # 計算訂單總金額
            total_amount = 0
            items_list = []

            for item in order_items:
                item_dict = dict(item)
                # 計算該項目總價
                item_dict['total_price'] = item_dict['quantity'] * item_dict['price']
                total_amount += item_dict['total_price']
                items_list.append(item_dict)

            # 將項目列表添加到訂單中
            order_dict['items'] = items_list
            order_dict['total_amount'] = total_amount

            orders_list.append(order_dict)

        return {"success": True, "orders": orders_list}
    except Exception as e:
        print(f"獲取訂單資料時發生錯誤: {e}")
        return {"success": False, "message": "獲取訂單資料時發生錯誤"}

def return_order(order_id):
    print(f"受理退貨申請: {order_id}")
    db = get_db()
    try:
        db.execute(
            'UPDATE orders SET order_status = "退貨中" WHERE order_id = ?',
            (order_id,)
        )
        db.commit()
        return {"success": True, "message": "退貨申請已提交，待審核"}
    except Exception as e:
        print(f"退貨申請時發生錯誤: {e}")
        db.rollback()
        return {"success": False, "message": "退貨申請時發生錯誤"}


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
