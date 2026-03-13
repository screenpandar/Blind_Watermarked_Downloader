from flask import Flask
from routes.user_routes import user_bp
from routes.file_routes import file_bp
from models.database import init_db

app = Flask(__name__)
app.config.from_object('config.Config')

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(file_bp, url_prefix='/file')

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
