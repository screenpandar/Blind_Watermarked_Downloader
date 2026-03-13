from models.database import get_db
from datetime import datetime
from config import Config
import time
import sqlite3

def log_request(user_id, username, filename, ip):
    with open(Config.LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()} - ID: {user_id} - User: {username} - IP: {ip} - File: {filename}\n")

def log_download(user_id, username, filename, ip):
    db = get_db()
    timestamp = datetime.now().isoformat()
    retry = 0

    while retry < 3:
        try:
            db.execute('INSERT INTO download_logs (user_id, username, filename, timestamp, ip) VALUES (?, ?, ?, ?, ?)',
            (user_id, username, filename, timestamp, ip))
            db.commit()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retry += 1
                time.sleep(1)
                print(f"[重试] 数据库写入失败，正在重试 ({retry}/3)...")
            else:
                raise e
    