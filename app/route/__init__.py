from flask import Blueprint

# 主要頁面路由
main_bp = Blueprint('main', __name__)

# 導入路由模組
from app.route import main_routes