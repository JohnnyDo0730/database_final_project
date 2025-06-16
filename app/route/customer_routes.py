from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app.route import customer_bp
from app.service.customer_service import *


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
    # 獲取書籍isbn、數量
    isbn = request.json.get('isbn')
    quantity = int(request.json.get('quantity'))

    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    try:
        if user_type != 'customer':
            return jsonify({'success': False, 'error': '非顧客用戶'}), 403
        if isbn is None or quantity is None:
            return jsonify({'success': False, 'error': 'isbn 或 數量不能為空'}), 400

        # 將書籍加入購物車
        isEnough = add_to_cart(user_id, isbn, quantity)

        if not isEnough:
            return jsonify({'success': True, 'message': '庫存可能不足，已加入購物車與補貨清單'})
        else:
            return jsonify({'success': True, 'message': '書籍加入購物車成功'})

    except Exception as e:
        print(f"書籍加入購物車失敗: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


#購物車頁：獲取購物車內容
@customer_bp.route('/customer/cart/content', methods=['GET'])
def customer_cart_content():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    try:
        if user_type != 'customer':
            return jsonify({'error': '非顧客用戶'}), 403

        # 獲取購物車內容
        cart_content = get_cart_content(user_id)

        # 返回購物車內容
        return jsonify({'cart_content': cart_content})

    except Exception as e:
        print(f"獲取購物車內容失敗: {e}")
        return jsonify({'error': str(e)}), 500


#購物車頁:送出訂單
@customer_bp.route('/customer/cart/submit')
def customer_cart_submit():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    try:
        if user_type != 'customer':
            return jsonify({'success': False, 'error': '非顧客用戶'}), 403
        
        # 發送訂單
        result = send_order(user_id)

        if result['success']:
            return jsonify({'success': True, 'message': '訂單送出成功'})
        else:
            return jsonify({'success': False, 'error': result['message']}), 500

    except Exception as e:
        print(f"訂單送出失敗: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


#購物車頁:商品移除購物車
@customer_bp.route('/customer/cart/remove', methods=['POST'])
def customer_cart_remove():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    isbn = request.json.get('isbn')

    try:
        if user_type != 'customer':
            return jsonify({'success': False, 'error': '非顧客用戶'}), 403

        # 移除購物車
        remove_from_cart(user_id, isbn)

        # 返回成功訊息
        return jsonify({'success': True, 'message': '商品移除購物車成功'})

    except Exception as e:
        print(f"商品移除購物車失敗: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


#訂單頁:獲取訂單記錄
@customer_bp.route('/customer/order_record/get_orders')
def customer_order_record_get_orders():
    # 獲取當前登入用戶的 user_id
    user_id = session.get('user_id')

    try:
        # 獲取該用戶的所有訂單
        result = get_user_orders(user_id)
        if result['success']:
            return jsonify({
                'success': True,
                'orders': result['orders']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 500
    except Exception as e:
        print(f"獲取訂單記錄失敗: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

        
#訂單頁:退貨
@customer_bp.route('/customer/order_record/return', methods=['POST'])
def customer_order_record_return():
    order_id = request.json.get('order_id')
    result = return_order(order_id)
    if result['success']:
        return jsonify({'success': True, 'message': result['message']})
    else:
        return jsonify({'success': False, 'error': result['message']}), 500


