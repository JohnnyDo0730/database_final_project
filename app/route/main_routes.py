from flask import render_template, request, redirect
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
def login():
    """登入"""
    username = request.form['username']
    password = request.form['password']
    user = get_user_by_username(username)
    if user and verify_password(user, password):
        if user['user_type'] == 'customer':
            return redirect('/customer')
        elif user['user_type'] == 'staff':
            return redirect('/backstage')
    return render_template('login.html')

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

