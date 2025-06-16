import requests
import json
import os

import random
import time

from dateutil import parser
from datetime import datetime


def normalize_publish_date(raw_date):
    if not raw_date:
        return "0000-01-01"  # 或 "未知"
    try:
        dt = parser.parse(raw_date)
        return dt.strftime('%Y-%m-%d')
    except Exception:
        return "0000-01-01"

def fetch_book_record(isbn):
    book_data = {
        'isbn': isbn,
        'title': '未知',
        'author': '未知',
        'publisher': '未知',
        'price': random.randint(200, 800),
        'stock': random.randint(5, 30),
        'type': '未知',
        'language': '未知',
        'publish_date': '未知'
    }

    # 主資料
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"無法獲取書籍主資料：{isbn}")
            return book_data
        data = resp.json()
        print(f"獲取書籍資料成功：{isbn}")
    except Exception as e:
        print(f"錯誤：{e}")
        return book_data

    # 書名與出版日
    book_data['title'] = data.get('title', '未知')
    book_data['publish_date'] = normalize_publish_date(data.get('publish_date', '未知'))

    # 出版商：取第一個
    publishers = data.get('publishers', [])
    book_data['publisher'] = publishers[0] if publishers else '未知'

    # 語言：轉為代碼並合併為字串
    languages = data.get('languages', [])
    language_list = [lang['key'].split('/')[-1] for lang in languages if 'key' in lang]
    book_data['language'] = ', '.join(language_list) if language_list else '未知'

    # 主題（subjects）：作為 type 使用
    subjects = data.get('subjects', [])
    book_data['type'] = ', '.join(subjects) if subjects else '未知'

    # 作者：需額外查詢
    authors = []
    for author in data.get('authors', []):
        key = author.get('key')
        if key:
            author_resp = requests.get(f'https://openlibrary.org{key}.json')
            if author_resp.status_code == 200:
                author_data = author_resp.json()
                authors.append(author_data.get('name', '未知作者'))
    book_data['author'] = ', '.join(authors) if authors else '未知'

    return book_data

def save_book_cover(isbn, save_dir=None):
    if save_dir is None:
        # 使用絕對路徑指向 app\static\images\book_covers
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images', 'book_covers')
        #print(save_dir)

    """下載指定 isbn 的書籍封面到指定目錄下，命名為 isbn.jpg"""
    # 封面來源（使用 Open Library 提供的封面服務）
    url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

    try:
        response = requests.get(url, timeout=5)
        # 檢查是否成功取得圖片（可能為 404 或非圖片）
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
            save_path = os.path.join(save_dir, f"{isbn}.jpg")
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"已儲存封面：{isbn}")
        else:
            print(f"無封面或非圖片格式：{isbn}")
    except Exception as e:
        print(f"封面下載失敗（isbn: {isbn}）：{e}")

def write_book_to_sql_file(book_data, file_path=os.path.join("app", "data", "real_books_schema.sql")):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            # 處理單引號轉義，避免 SQL 錯誤
            def esc(val):
                return str(val).replace("'", "''") if val is not None else ''

            sql = f"""INSERT INTO books (isbn, title, author, publisher, price, stock, type, language, publish_date)
                        VALUES ('{esc(book_data['isbn'])}', '{esc(book_data['title'])}', '{esc(book_data['author'])}',
                                '{esc(book_data['publisher'])}', {book_data['price']}, {book_data['stock']},
                                '{esc(book_data['type'])}', '{esc(book_data['language'])}', '{esc(book_data['publish_date'])}');\n"""

            f.write(sql)
            print(f"✅ 已寫入 SQL 檔案：{book_data['isbn']}")
    except Exception as e:
        print(f"❌ 寫入 SQL 檔案失敗（isbn: {book_data['isbn']}）：{e}")


def load_isbns_from_file(file_path=os.path.join("app", "data", "isbn_list.txt")):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    isbns = load_isbns_from_file()
    count = 0

    for isbn in isbns:
        try:
            record = fetch_book_record(isbn)
            if record:
                #db = get_db()
                #insert_book_to_db(record, db)
                write_book_to_sql_file(record)
                save_book_cover(isbn)
                #db.close()
                print(f"✅ 處理成功：{isbn}")
                count += 1
            else:
                print(f"⚠️ 無資料：{isbn}")
        except Exception as e:
            print(f"❌ 處理失敗 {isbn}：{e}")
        time.sleep(0.3)  # 延遲 300ms，減少 API 負擔

    print(f"✅ 共 {count} 本書加入成功")