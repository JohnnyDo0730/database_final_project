from flask import render_template, request, jsonify, session
from app.route import backstage_bp
from app.service.backstage_service import *

''' 後台頁面模板 '''
@backstage_bp.route('/backstage')
def backstage_page():
    return render_template('backstage_base.html')

''' 後台頁面子頁 '''
#後台書籍頁面
@backstage_bp.route('/backstage/book')
def backstage_book_page():
    return render_template('backstage/book.html')

#後台採購購物車頁面
@backstage_bp.route('/backstage/purchase_cart')
def backstage_purchase_cart_page():
    return render_template('backstage/purchase_cart.html')

#後台退貨頁面
@backstage_bp.route('/backstage/return')
def backstage_return_page():
    return render_template('backstage/return.html')

#後台補貨頁面
@backstage_bp.route('/backstage/reorder')
def backstage_reorder_page():
    return render_template('backstage/reorder.html')

#後台採購紀錄頁面
@backstage_bp.route('/backstage/purchase_record')
def backstage_purchase_record_page():
    return render_template('backstage/purchase_record.html')


''' 後台頁面功能 '''
# 書籍頁: 獲取當前頁之書籍列表、總頁數
@backstage_bp.route('/backstage/book/content', methods=['GET'])
def backstage_book_content():
    # 獲取搜尋關鍵字、頁數
    search_keyword = request.args.get('search_keyword', '', type=str)
    page = request.args.get('page', 1, type=int)

    try:
        # 獲取書籍列表
        book_list = get_book_list(search_keyword, page, items_per_page=10)
        # 獲取總頁數
        total_pages = get_total_pages(search_keyword, items_per_page=10)

        # 返回書籍列表和總頁數
        return jsonify({'book_list': book_list, 'total_pages': total_pages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#書籍頁:加入購物車
@backstage_bp.route('/backstage/book/add_to_cart', methods=['POST'])
def backstage_book_add_to_cart():
    # 獲取書籍ISBN、數量
    isbn = request.json.get('isbn')
    quantity = int(request.json.get('quantity'))

    user_id = session.get('user_id')
    user_type = session.get('user_type')
    try:
        if user_type != 'staff':
            return jsonify({'error': '非後台用戶'}), 403

        if isbn is None or quantity is None:
            return jsonify({'error': 'ISBN 或 數量不能為空'}), 400

        # 將書籍加入購物車
        add_to_cart(user_id, isbn, quantity)

        # 返回成功訊息
        return jsonify({'message': '書籍加入購物車成功'})
    except Exception as e:
        print(f"書籍加入購物車失敗: {e}")
        return jsonify({'error': str(e)}), 500


#購物車頁：獲取購物車內容
@backstage_bp.route('/backstage/purchase_cart/content', methods=['GET'])
def backstage_purchase_cart_content():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    try:
        if user_type != 'staff':
            return jsonify({'error': '非後台用戶'}), 403

        # 獲取購物車內容
        cart_content = get_cart_content(user_id)

        # 返回購物車內容
        return jsonify({'cart_content': cart_content})

    except Exception as e:
        print(f"獲取購物車內容失敗: {e}")
        return jsonify({'error': str(e)}), 500


#購物車頁:送出訂單
@backstage_bp.route('/backstage/purchase_cart/submit')
def backstage_purchase_cart_submit():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    try:
        if user_type != 'staff':
            return jsonify({'success': False, 'error': '非後台用戶'}), 403
        
        # 發送訂單
        result = send_purchase_order(user_id)

        if result['success']:
            return jsonify({'success': True, 'message': '訂單送出成功'})
        else:
            return jsonify({'success': False, 'error': result['message']}), 500

    except Exception as e:
        print(f"訂單送出失敗: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


#購物車頁:商品移除購物車
@backstage_bp.route('/backstage/purchase_cart/remove', methods=['POST'])
def backstage_purchase_cart_remove():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    isbn = request.json.get('isbn')

    try:
        if user_type != 'staff':
            return jsonify({'error': '非後台用戶'}), 403

        # 移除購物車
        remove_from_purchase_cart(user_id, isbn)

        # 返回成功訊息
        return jsonify({'message': '商品移除購物車成功'})

    except Exception as e:
        print(f"商品移除購物車失敗: {e}")
        return jsonify({'error': str(e)}), 500



#退貨頁:同意退貨
@backstage_bp.route('/backstage/return/confirm', methods=['POST'])
def backstage_return_confirm():
    raise NotImplementedError


#退貨頁:拒絕退貨
@backstage_bp.route('/backstage/return/reject', methods=['POST'])
def backstage_return_reject():
    raise NotImplementedError


#補貨頁:加入購物車
@backstage_bp.route('/backstage/reorder/add_to_cart', methods=['POST'])
def backstage_reorder_add_to_cart():
    raise NotImplementedError



#訂單頁:獲取訂單記錄
@backstage_bp.route('/backstage/purchase_record/get_orders')
def backstage_purchase_record_get_orders():

    try:
        # 獲取該用戶的所有訂單
        result = get_purchase_orders()
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

        
#採購紀錄頁:簽收
@backstage_bp.route('/backstage/purchase_record/sign', methods=['POST'])
def backstage_purchase_record_sign():
    order_id = request.json.get('order_id')
    result = sign_purchase_order(order_id)
    if result['success']:
        return jsonify({'success': True, 'message': result['message']})
    else:
        return jsonify({'success': False, 'error': result['message']}), 500