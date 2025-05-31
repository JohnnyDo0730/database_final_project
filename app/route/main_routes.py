from flask import render_template, request, redirect, jsonify
from app.route import main_bp
from app.service.user_service import get_user_by_username, verify_password


@main_bp.route('/')
def login_page():
    """首頁"""
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    """註冊頁面"""
    return render_template('register.html')

@main_bp.route('/login', methods=['POST'])
# 正式登入
# def login():
#     """登入"""
#     username = request.form['username']
#     password = request.form['password']
#     user = get_user_by_username(username)
#     if user and verify_password(user, password):
#         if user['user_type'] == 'customer':
#             return redirect('/customer')
#         elif user['user_type'] == 'staff':
#             return redirect('/backstage')
#     return render_template('login.html')

# 測試登入
def login():
    """登入"""
    # 取得使用者選擇的身份類型
    user_type = request.form['user_type']
    
    # 直接根據身份類型跳轉，不檢查使用者名稱和密碼
    if user_type == 'customer':
        return redirect('/customer')
    elif user_type == 'staff':
        return redirect('/backstage')
    
    # 若有問題，回到登入頁面
    return render_template('login.html')

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """處理用戶登出"""
    # 這裡可以添加會話管理，如果將來實施
    # 例如：清除 session 或 cookie
    
    # 無論是 GET 還是 POST 請求，都直接重定向到登入頁面
    return redirect('/')

@main_bp.route('/register', methods=['POST'])
def register():
    """註冊"""
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['user_type']
    if user_type == 'customer':
        email = request.form['email']
        address = request.form['address']
        user_id = create_user(username, password, user_type, email, address)
    elif user_type == 'staff':
        user_id = create_user(username, password, user_type)
    return redirect('/')

