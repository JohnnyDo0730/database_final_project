from flask import render_template
from app.route import main_bp

@main_bp.route('/')
def index():
    """首頁"""
    return render_template('index.html')