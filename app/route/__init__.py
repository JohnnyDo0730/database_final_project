from flask import Blueprint

# 主要頁面路由
main_bp = Blueprint('main', __name__)
customer_bp = Blueprint('customer', __name__)
backstage_bp = Blueprint('backstage', __name__)

# 導入路由模組
from app.route import login_routes
from app.route import customer_routes
from app.route import backstage_routes