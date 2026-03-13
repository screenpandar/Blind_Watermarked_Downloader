import os

class Config:
    # 优先从环境变量读取，便于部署与开源（可配合 .env.example）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    DATABASE = os.environ.get('DATABASE', 'data_center.db')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
    LOG_FILE = os.path.join(os.getcwd(), 'logs', 'access.log')
