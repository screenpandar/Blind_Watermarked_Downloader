from models.database import get_db
import random

def generate_user_id(length=10):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def register_user(username, password):
    db = get_db()
    try:
        while True:
            user_id = generate_user_id()
            existing = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
            if not existing:
                break

        db.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)', (user_id, username, password))
        db.commit()
        return {'status': 'success', 'message': '注册成功', 'user_id': user_id}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def validate_user_and_get_id(username, password):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if user:
        return user['user_id']
    return None

