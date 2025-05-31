-- 插入測試買家用戶
INSERT INTO users (name, password, user_type) 
VALUES ('test_customer', 'pbkdf2:sha256:600000$ZGHRbxKL3TSwaCzR$0f58b53b67d94d3f4dafd7b7b4d60b56df33a0845d5e4fc11c963d7d0a2c71ba', 'customer');

-- 獲取剛插入的買家用戶 ID
INSERT INTO customer (user_id, email, address) 
VALUES (last_insert_rowid(), 'customer@example.com', '台北市信義區101號');

-- 插入測試店員用戶
INSERT INTO users (name, password, user_type) 
VALUES ('test_staff', 'pbkdf2:sha256:600000$ZGHRbxKL3TSwaCzR$0f58b53b67d94d3f4dafd7b7b4d60b56df33a0845d5e4fc11c963d7d0a2c71ba', 'staff');

-- 獲取剛插入的店員用戶 ID
INSERT INTO staff (user_id) 
VALUES (last_insert_rowid());
