import os
import random
from datetime import datetime, timedelta

def generate_fake_orders_sql(file_path=os.path.join("app", "data", "fake_data_schema.sql")):

    old_statuses = (
        ["已送達，不接受退貨(超過7天鑑賞期)"] * 80 +
        ["已退貨"] * 20
    )
    new_statuses = (
        ["退貨中"] * 20 + 
        ["已送達"] * 80
    )

    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 5, 15)
    today = datetime.today()

    def random_old_date():
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

    def recent_date_within_7_days():
        days_ago = random.randint(0, 6)  # 包含今天
        return (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')

    values = []

    # 前 50 筆（舊資料）
    for _ in range(50):
        user_id = random.randint(1, 50)
        order_date = random_old_date()
        status = random.choice(old_statuses)
        values.append(f"({user_id}, '{order_date}', '{status}')")

    # 接著 50 筆（近七日、已送達/退貨中）
    for _ in range(50):
        user_id = random.randint(1, 50)
        order_date = recent_date_within_7_days()
        status = random.choice(new_statuses)
        values.append(f"({user_id}, '{order_date}', '{status}')")


    # 組合 SQL
    sql_lines = ["-- 插入訂單數據\n", "INSERT INTO orders (user_id, order_date, order_status) VALUES\n"]
    for i, v in enumerate(values):
        end = ";\n" if i == len(values) - 1 else ",\n"
        sql_lines.append(v + end)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 已將 100 筆訂單資料寫入到 {file_path}")


def generate_fake_order_items_sql(
    file_path=os.path.join("app", "data", "fake_data_schema.sql"),
    isbn_path=os.path.join("app", "data", "isbn_list.txt"),
    order_count=100
):
    # 讀取 isbn 清單
    with open(isbn_path, "r", encoding="utf-8") as f:
        isbns = [line.strip() for line in f if line.strip()]
    
    if len(isbns) < 1:
        raise ValueError("❌ isbn 清單為空，請確認 isbn_list.txt 是否存在有效內容")

    sql_lines = ["-- 插入訂單項目數據\n", "INSERT INTO order_items (order_id, isbn, quantity) VALUES\n"]

    entries = []
    for order_id in range(1, order_count + 1):
        book_count = random.randint(1, 3)
        used_isbns = random.sample(isbns, min(book_count, len(isbns)))

        for isbn in used_isbns:
            quantity = random.randint(1, 5)
            entries.append(f"({order_id}, '{isbn}', {quantity})")

    for i, line in enumerate(entries):
        end = ";\n" if i == len(entries) - 1 else ",\n"
        sql_lines.append(line + end)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 已將訂單項目資料寫入到 {file_path}（共 {len(entries)} 筆）")


def generate_fake_purchase_orders_sql(
    file_path=os.path.join("app", "data", "fake_data_schema.sql"),
    purchase_count=100
):
    sql_lines = ["-- 插入採購訂單數據\n", "INSERT INTO purchases_orders (user_id, purchase_date, purchase_status) VALUES\n"]

    entries = []
    for _ in range(purchase_count):
        user_id = random.randint(51, 100)
        # 日期設為 2025 年初的 1~4 月
        start_date = datetime(2025, 1, 1)
        random_days = random.randint(0, 120)  # 1~4月範圍
        purchase_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        status = random.choice(["已申請", "已簽收"])
        entries.append(f"({user_id}, '{purchase_date}', '{status}')")

    for i, line in enumerate(entries):
        sql_lines.append(line + (";\n" if i == len(entries) - 1 else ",\n"))

    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 採購訂單資料寫入成功，共 {purchase_count} 筆")


def generate_fake_po_items_sql(
    file_path=os.path.join("app", "data", "fake_data_schema.sql"),
    isbn_path=os.path.join("app", "data", "isbn_list.txt"),
    purchase_count=100
):
    # 讀取 isbn 清單
    with open(isbn_path, "r", encoding="utf-8") as f:
        isbns = [line.strip() for line in f if line.strip()]
    
    if not isbns:
        raise ValueError("❌ isbn 清單為空，請確認 app/data/isbn_list.txt")

    sql_lines = ["-- 插入採購訂單項目數據\n", "INSERT INTO po_items (purchase_id, isbn, quantity) VALUES\n"]

    entries = []
    for purchase_id in range(1, purchase_count + 1):
        book_count = random.randint(1, 3)
        chosen_isbns = None
        while chosen_isbns is None or '9780312152130' in chosen_isbns:  # 測試補貨用，跳過
            chosen_isbns = random.sample(isbns, min(book_count, len(isbns)))
        for isbn in chosen_isbns:
            quantity = random.randint(10, 50)
            entries.append(f"({purchase_id}, '{isbn}', {quantity})")

    for i, line in enumerate(entries):
        sql_lines.append(line + (";\n" if i == len(entries) - 1 else ",\n"))

    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 採購訂單項目資料寫入成功，共 {len(entries)} 筆")


def generate_cart_sql(
    file_path=os.path.join("app", "data", "fake_data_schema.sql"),
    isbn_path=os.path.join("app", "data", "isbn_list.txt"),
    count=100
):
    # 讀取 isbn 清單
    with open(isbn_path, "r", encoding="utf-8") as f:
        isbn_list = [line.strip() for line in f if line.strip()]
    
    if not isbn_list:
        print("❌ 找不到 isbn 清單")
        return

    sql_lines = ["-- 插入一般用戶購物車資料\n", "INSERT INTO cart (user_id, isbn, quantity) VALUES\n"]
    
    for i in range(count):
        user_id = random.randint(1, 50)
        isbn = random.choice(isbn_list)
        quantity = random.randint(1, 5)
        end = ";\n" if i == count - 1 else ",\n"
        sql_lines.append(f"({user_id}, '{isbn}', {quantity}){end}")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 已將 {count} 筆一般用戶購物車資料寫入到 {file_path}")


def generate_purchase_cart_sql(
    file_path=os.path.join("app", "data", "fake_data_schema.sql"),
    isbn_path=os.path.join("app", "data", "isbn_list.txt"),
    count=100
):
    # 讀取 isbn 清單
    with open(isbn_path, "r", encoding="utf-8") as f:
        isbn_list = [line.strip() for line in f if line.strip()]
    
    if not isbn_list:
        print("❌ 找不到 isbn 清單")
        return
    
    sql_lines = ["-- 插入採購購物車資料\n", "INSERT INTO purchase_cart (user_id, isbn, quantity) VALUES\n"]
    
    for i in range(count):
        user_id = random.randint(51, 100)
        isbn = random.choice(isbn_list)
        quantity = random.randint(5, 50)
        end = ";\n" if i == count - 1 else ",\n"
        sql_lines.append(f"({user_id}, '{isbn}', {quantity}){end}")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.writelines(sql_lines)

    print(f"✅ 已將 {count} 筆採購購物車資料寫入到 {file_path}")


if __name__ == "__main__":
    generate_fake_orders_sql()
    generate_fake_order_items_sql()
    generate_fake_purchase_orders_sql()
    generate_fake_po_items_sql()
    generate_cart_sql()
    generate_purchase_cart_sql()
