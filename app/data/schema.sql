-- 刪除現有表格（如果存在）
DROP TABLE IF EXISTS restock;
DROP TABLE IF EXISTS order_pending;
DROP TABLE IF EXISTS purchase_pending;
DROP TABLE IF EXISTS po_items;
DROP TABLE IF EXISTS purchases_orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS users;

-- 創建用戶表
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  user_type TEXT NOT NULL CHECK(user_type IN ('customer', 'staff')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE staff (
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE customer (
  user_id INTEGER NOT NULL,
  email TEXT UNIQUE,
  address TEXT,
  balance REAL NOT NULL DEFAULT 500,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- 創建書籍表
CREATE TABLE books (
  ISBN INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  publisher TEXT NOT NULL,
  price REAL NOT NULL,
  stock INTEGER NOT NULL,
  type TEXT NOT NULL,
  language TEXT NOT NULL,
  publish_date DATE NOT NULL
);

-- 訂單: 已送達,已送達，不接受退貨(超過7天鑑賞期),退貨中, 已退貨
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  order_date DATE NOT NULL,
  order_status TEXT,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE order_items (
  order_id INTEGER NOT NULL,
  ISBN INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders (order_id),
  FOREIGN KEY (ISBN) REFERENCES books (ISBN)
);

CREATE TABLE cart (
  user_id INTEGER NOT NULL,
  isbn INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (isbn) REFERENCES books (ISBN),
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- 採購訂單: 已申請,已簽收
CREATE TABLE purchases_orders (
  purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  purchase_date DATE NOT NULL,
  purchase_status TEXT,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE po_items (
  purchase_id INTEGER NOT NULL,
  ISBN INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (purchase_id) REFERENCES purchases_orders (purchase_id),
  FOREIGN KEY (ISBN) REFERENCES books (ISBN)
);

CREATE TABLE purchase_cart (
  user_id INTEGER NOT NULL,
  isbn INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (isbn) REFERENCES books (ISBN),
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- purchase 待簽收
CREATE TABLE purchase_pending (
  purchase_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (purchase_id) REFERENCES purchases_orders (purchase_id),
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- order 待退貨
CREATE TABLE order_pending (
  order_id INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

-- 補貨
CREATE TABLE restock (
  ISBN INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (ISBN) REFERENCES books (ISBN)
);


