from flask import render_template
from app.route import customer_bp

''' 客戶頁面模板 '''
@customer_bp.route('/customer')
def customer_page():
    """客戶頁面"""
    return render_template('customer.html')

''' 客戶頁面子頁 '''
#客戶書籍頁面
@customer_bp.route('/customer/book')
def customer_book_page():
    return render_template('customer_book.html')

#客戶購物車頁面
@customer_bp.route('/customer/cart')
def customer_cart_page():
    return render_template('customer_cart.html')

#客戶訂單紀錄頁面
@customer_bp.route('/customer/order_record')
def customer_order_record_page():
    return render_template('customer_order_record.html')


''' 客戶頁面功能 '''
#書籍頁:搜尋
@customer_bp.route('/customer/book/search', methods=['POST'])


#書籍頁:商品加入購物車
@customer_bp.route('/customer/book/add_to_cart', methods=['POST'])


#購物車頁:商品移除購物車
@customer_bp.route('/customer/cart/remove_from_cart', methods=['POST'])


#購物車頁:結帳
@customer_bp.route('/customer/cart/checkout', methods=['POST'])


#訂單頁:退貨
@customer_bp.route('/customer/order/return', methods=['POST'])
