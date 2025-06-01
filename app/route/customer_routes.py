from flask import render_template, request, session, redirect, url_for, flash
from app.route import customer_bp
from app.service.customer_service import get_customer_profile_by_username, get_customer_profile_by_user_id
from app.service.user_service import get_user_by_username

''' 客戶頁面模板 '''
@customer_bp.route('/customer')
def customer_page():
    # 檢查用戶是否已登入
    if not session.get('logged_in') or session.get('user_type') != 'customer':
        return redirect('/')
    return render_template('customer_base.html')

''' 客戶頁面子頁 '''
#客戶書店瀏覽頁面
@customer_bp.route('/customer/store')
def customer_store_page():
    return render_template('customer/store.html')

#客戶購物車頁面
@customer_bp.route('/customer/cart')
def customer_cart_page():
    return render_template('customer/cart.html')

#客戶訂單紀錄頁面(包含退貨按鈕)
@customer_bp.route('/customer/order_record')
def customer_order_record_page():
    return render_template('customer/order_record.html')


#客戶個人資料頁面
@customer_bp.route('/customer/profile')
def customer_profile_page():
    # 檢查用戶是否已登入
    if not session.get('logged_in') or session.get('user_type') != 'customer':
        return redirect('/')
    
    # 從 session 中獲取當前登入用戶的 user_id
    user_id = session.get('user_id')
    
    # 使用 user_id 獲取完整的顧客資料
    profile = get_customer_profile_by_user_id(user_id) if user_id else None
    
    return render_template('customer/profile.html', profile=profile)


''' 客戶頁面功能 '''
#書籍頁:搜尋
@customer_bp.route('/customer/store/search', methods=['POST'])
def customer_store_search():
    raise NotImplementedError



#書籍頁:商品加入購物車
@customer_bp.route('/customer/store/add_to_cart', methods=['POST'])
def customer_store_add_to_cart():
    raise NotImplementedError


#購物車頁:商品移除購物車
@customer_bp.route('/customer/cart/remove_from_cart', methods=['POST'])
def customer_cart_remove_from_cart():
    raise NotImplementedError


#購物車頁:結帳
@customer_bp.route('/customer/cart/checkout', methods=['POST'])
def customer_cart_checkout():
    raise NotImplementedError


#訂單頁:退貨
@customer_bp.route('/customer/order_record/return', methods=['POST'])
def customer_order_record_return():
    raise NotImplementedError


