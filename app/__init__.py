from flask import Flask
from flask_cors import CORS

def create_app(config=None):
    """
    應用程式工廠函數，用於創建和配置 Flask 應用
    """
    app = Flask(__name__)
    
    # 啟用 CORS
    CORS(app)
    
    # 配置應用
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='database_final_project',
    )
    
    if config:
        app.config.update(config)
    
    # 註冊藍圖
    from app.route import main_bp, api_bp
    app.register_blueprint(main_bp)
    
    # 初始化資料庫連接
    #from app.util.db import init_app
    #init_app(app)
    
    return app 