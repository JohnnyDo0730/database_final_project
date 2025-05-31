from flask import render_template
from app.route import customer_bp

''' 客戶頁面模板 '''
@customer_bp.route('/customer')
def customer_page():
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
    return render_template('customer/profile.html')


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


