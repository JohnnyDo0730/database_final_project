from flask import render_template
from app.route import customer_bp

@customer_bp.route('/customer')
def customer_page():
    """客戶頁面"""
    return render_template('customer.html')