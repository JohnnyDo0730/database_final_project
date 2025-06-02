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
    return total_pages//items_per_page + 1

def add_to_cart(isbn, quantity):
    db = get_db()
    db.execute(
        'INSERT INTO purchase_cart (isbn, quantity) VALUES (?, ?)',
        (isbn, quantity)
    )
    db.commit()
    
    print(f"書籍 ISBN: {isbn}, 數量: {quantity} 已加入訂單購物車")
