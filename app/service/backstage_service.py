from app.util.db import get_db
from datetime import datetime
from flask import session


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

            # 建立訂單紀錄
            add_to_purchase_order(user_id, book_list, need_commit=False)

            db.commit()

            return {"success": True, "message": "訂單建立成功"}
        else:
            # 如果購物車沒有商品，則返回錯誤訊息
            return {"success": False, "message": "購物車沒有商品"}

    except Exception as e:
        print(f"訂單送出失敗: {e}")
        db.rollback()
        return {"success": False, "message": "訂單送出失敗"}

def add_to_purchase_order(user_id, book_list, need_commit=True):
    db = get_db()

    try:
        # 建立訂單紀錄
        db.execute(
            'INSERT INTO purchases_orders (user_id, purchase_date, purchase_status) VALUES (?, ?, ?)',
            (user_id, datetime.now().strftime('%Y-%m-%d'), '已申請')
        )

        # 取得訂單編號
        order_id = db.execute(
            'SELECT last_insert_rowid()'
        ).fetchone()[0]

        # 建立訂單項目紀錄
        for book in book_list:
            db.execute(
                'INSERT INTO po_items (purchase_id, isbn, quantity) VALUES (?, ?, ?)',
                (order_id, book['isbn'], book['quantity'])
            )

        if need_commit:
            db.commit()

        print(f"訂單建立成功，訂單編號: {order_id}")
        return {"success": True, "message": "訂單建立成功"}
    except Exception as e:
        db.rollback()
        print(f"建立訂單時發生錯誤: {e}")
        raise e

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


''' 訂單查詢頁 '''
def get_purchase_orders():

    db = get_db()
    try:
        # 獲取所有訂單
        orders = db.execute(
            'SELECT user_id, purchase_id, purchase_date, purchase_status FROM purchases_orders ORDER BY purchase_id DESC',
        ).fetchall()

        # 將結果轉換為字典列表
        orders_list = []

        for order in orders:
            order_dict = dict(order)

            # 獲取該訂單的所有項目
            order_items = db.execute(
                'SELECT oi.isbn, oi.quantity, b.title, b.price ' 
                'FROM po_items oi '
                'JOIN books b ON oi.isbn = b.isbn '
                'WHERE oi.purchase_id = ?',
                (order_dict['purchase_id'],)
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

def sign_purchase_order(purchase_id):
    print(f"受理簽收: {purchase_id}")
    db = get_db()
    try:
        db.execute(
            'UPDATE purchases_orders SET purchase_status = "已簽收" WHERE purchase_id = ?',
            (purchase_id,)
        )

        # 更新庫存
        order_items = db.execute(
            'SELECT isbn, quantity FROM po_items WHERE purchase_id = ?',
            (purchase_id,)
        ).fetchall()
        for item in order_items:
            db.execute(
                'UPDATE books SET stock = stock + ? WHERE isbn = ?',
                (item['quantity'], item['isbn'])
            )

        db.commit()
        return {"success": True, "message": "簽收成功"}
    except Exception as e:
        print(f"簽收時發生錯誤: {e}")
        db.rollback()
        return {"success": False, "message": "簽收時發生錯誤"}


''' 退貨頁 '''
def get_return_orders(user_name=None):
    db = get_db()
    try:
        # 獲取退貨中的訂單
        return_orders = db.execute("""
            SELECT order_id, order_date, order_status, user_id
            FROM orders
            WHERE order_status = '退貨中'
            ORDER BY order_date DESC
        """).fetchall()
        
        result = []
        for order in return_orders:
            order_dict = dict(order)
            
            # 獲取訂單項目
            order_items = db.execute("""
                SELECT oi.isbn, oi.quantity, b.title, b.price
                FROM order_items oi
                JOIN books b ON oi.isbn = b.isbn
                WHERE oi.order_id = ?
            """, (order_dict['order_id'],)).fetchall()
            
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
            
            result.append(order_dict)
            
        return result
    except Exception as e:
        print(f"獲取退貨訂單時發生錯誤: {e}")
        return []

def confirm_return(order_id):
    db = get_db()
    try:
        # 確認退貨前檢查訂單狀態和用戶信息
        order = db.execute(
            'SELECT o.order_id, o.order_status, o.user_id FROM orders o WHERE o.order_id = ?',
            (order_id,)
        ).fetchone()
        
        if not order:
            return {"success": False, "message": "訂單不存在"}
            
        if order['order_status'] != '退貨中':
            return {"success": False, "message": "該訂單不是退貨中狀態"}
        
        # 計算訂單總金額
        order_items = db.execute(
            'SELECT oi.isbn, oi.quantity, b.price FROM order_items oi '
            'JOIN books b ON oi.isbn = b.isbn '
            'WHERE oi.order_id = ?',
            (order_id,)
        ).fetchall()
        
        total_refund = 0
        for item in order_items:
            item_total = item['quantity'] * item['price']
            total_refund += item_total
            
            # 更新庫存
            db.execute(
                'UPDATE books SET stock = stock + ? WHERE isbn = ?',
                (item['quantity'], item['isbn'])
            )
        
        # 更新訂單狀態為已退貨
        db.execute(
            'UPDATE orders SET order_status = "已退貨" WHERE order_id = ?',
            (order_id,)
        )
        
        # 更新客戶餘額
        db.execute(
            'UPDATE customer SET balance = balance + ? WHERE user_id = ?',
            (total_refund, order['user_id'])
        )
        
        print(f"退款金額: {total_refund} 元已加到用戶 {order['user_id']} 的帳戶餘額")
        
        db.commit()
        return {"success": True, "message": "退貨已確認，退款已加到客戶帳戶"}
    except Exception as e:
        print(f"確認退貨時發生錯誤: {e}")
        db.rollback()
        return {"success": False, "message": "確認退貨時發生錯誤"}
        
def reject_return(order_id, reason=''):
    db = get_db()
    try:
        # 拒絕退貨前檢查訂單狀態
        order = db.execute(
            'SELECT order_status FROM orders WHERE order_id = ?',
            (order_id,)
        ).fetchone()
        
        if not order:
            return {"success": False, "message": "訂單不存在"}
            
        if order['order_status'] != '退貨中':
            return {"success": False, "message": "該訂單不是退貨中狀態"}
        
        # 更新訂單狀態為已完成
        db.execute(
            'UPDATE orders SET order_status = "已完成" WHERE order_id = ?',
            (order_id,)
        )
        
        db.commit()
        return {"success": True, "message": "退貨已拒絕"}
    except Exception as e:
        print(f"拒絕退貨時發生錯誤: {e}")
        db.rollback()
        return {"success": False, "message": "拒絕退貨時發生錯誤"}

''' 補貨 ''' # 加入購物車後需要移除補貨清單
def get_restock_list():
    db = get_db()
    try:
        restock_list = db.execute(
            'SELECT r.isbn, r.quantity, b.title FROM restock as r JOIN books as b ON r.isbn = b.isbn',
        ).fetchall()
        restock_list_dict = [dict(row) for row in restock_list]
        return {"success": True, "restock_list": restock_list_dict}
    except Exception as e:
        print(f"獲取補貨清單時發生錯誤: {e}")
        return {"success": False, "message": "獲取補貨清單時發生錯誤"}

def add_to_purchase_cart_restock(isbn):
    db = get_db()
    try:
        # 檢查是否在補貨清單
        restock_list = db.execute(
            'SELECT isbn, quantity FROM restock WHERE isbn = ?',
            (isbn,)
        ).fetchone()
        if not restock_list:
            raise Exception("補貨清單不存在")

        # 先檢查是否已有這本書在購物車
        existing = db.execute(
            'SELECT quantity FROM purchase_cart WHERE isbn = ?',
            (isbn,)
        ).fetchone()
        
        user_id = session.get('user_id')
        if existing:
            # 如果已存在，則更新數量
            db.execute(
                'UPDATE purchase_cart SET quantity = quantity + ? WHERE isbn = ? AND user_id = ?',
                (restock_list['quantity'], isbn, user_id)
            )
        else:
            # 如果不存在，則新增
            db.execute(
                'INSERT INTO purchase_cart (isbn, quantity, user_id) VALUES (?, ?, ?)',
                (isbn, restock_list['quantity'], user_id)
            )

        # 刪除補貨清單 
        db.execute(
                'DELETE FROM restock WHERE isbn = ?',
                (isbn,)
        )
        db.commit()
        return {"success": True, "message": "補貨清單已移到購物車"}
        
    except Exception as e:
        print(f"加入購物車時發生錯誤: {e}")
        db.rollback()
        return {"success": False, "message": "加入購物車時發生錯誤"}
