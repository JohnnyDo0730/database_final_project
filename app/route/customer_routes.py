from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app.route import customer_bp
from app.service.customer_service import get_customer_profile_by_username, get_customer_profile_by_user_id, get_book_list, get_total_pages, add_to_cart
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
#書籍頁:獲取書籍列表
@customer_bp.route('/customer/store/content')
def customer_store_content():
    search_keyword = request.args.get('search_keyword', '')
    page = int(request.args.get('page', 1))
    
    try:
        # 獲取符合關鍵字的書籍
        books = get_book_list(search_keyword, page, items_per_page=12)
        # 獲取總頁數
        total_pages = get_total_pages(search_keyword, items_per_page=12)
        
        return jsonify({
            'book_list': books,
            'total_pages': total_pages
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


#書籍頁:商品加入購物車
@customer_bp.route('/customer/store/add_to_cart', methods=['POST'])
def customer_store_add_to_cart():
    # 獲取書籍ISBN、數量
    isbn = request.json.get('isbn')
    quantity = int(request.json.get('quantity'))

    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    try:
        if user_type != 'customer':
            return jsonify({'error': '非顧客用戶'}), 403
        if isbn is None or quantity is None:
            return jsonify({'error': 'ISBN 或 數量不能為空'}), 400

        # 將書籍加入購物車
        add_to_cart(user_id, isbn, quantity)

        # 返回成功訊息
        return jsonify({'message': '書籍加入購物車成功'})
    except Exception as e:
        print(f"書籍加入購物車失敗: {e}")
        return jsonify({'error': str(e)}), 500


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


