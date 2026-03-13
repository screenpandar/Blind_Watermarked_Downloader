import os
import csv
from datetime import datetime
from models.database import get_db
from flask import Flask

#  创建 Flask 应用，并导入配置
app = Flask(__name__)
app.config.from_object('config.Config')

EXPORT_FOLDER = os.path.join(os.getcwd(), 'exports')
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def export_download_logs():
    with app.app_context():  # ✅ 进入 Flask 应用上下文
        db = get_db()
        logs = db.execute('SELECT * FROM download_logs').fetchall()

        filename = f"download_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(EXPORT_FOLDER, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'User ID', 'Filename', 'Timestamp', 'IP'])

            for log in logs:
                writer.writerow([log['id'], log['user_id'], log['filename'], log['timestamp'], log['ip']])

        print(f"✅ 日志已导出至：{filepath}")

if __name__ == "__main__":
    export_download_logs()
