from flask import render_template
from app.route import backstage_bp

@backstage_bp.route('/backstage')
def backstage_page():
    """後台頁面"""
    return render_template('backstage.html')