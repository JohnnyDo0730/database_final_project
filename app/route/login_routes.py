from flask import render_template, request, redirect, jsonify, session
from app.route import main_bp
from app.service.user_service import get_user_by_username, verify_password, create_user


@main_bp.route('/')
def login_page():
    """首頁"""
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    """註冊頁面"""
    return render_template('register.html')

@main_bp.route('/login', methods=['POST'])
def login():
    """登入驗證"""
    # 取得使用者選擇的身份類型和登入資訊
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']
    
    # 從資料庫中檢查用戶
    user = get_user_by_username(username)
    
    # 驗證用戶密碼和類型
    if user and verify_password(user, password) and user['user_type'] == user_type:
        # 登入成功，將用戶信息存入 session
        session['logged_in'] = True
        session['username'] = username
        session['user_type'] = user_type
        session['user_id'] = user['user_id']
        
        # 跳轉到相應頁面
        if user_type == 'customer':
            return redirect('/customer')
        elif user_type == 'staff':
            return redirect('/backstage')
    
    # 登入失敗，顯示錯誤訊息
    error_message = "帳號或密碼輸入錯誤，請重新輸入"
    return render_template('login.html', error=error_message)

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """處理用戶登出"""
    # 清除 session 中的所有用戶信息
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_type', None)
    session.pop('user_id', None)
    
    # 重定向到登入頁面
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
