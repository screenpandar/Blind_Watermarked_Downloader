from flask import Blueprint, request, jsonify
from services.user_service import register_user, validate_user_and_get_id

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = register_user(username, password)
    return jsonify(result)


@user_bp.route('/login', methods=['POST'])
def login():
    """
    简单登录接口：仅用于校验用户名和密码是否匹配，
    成功时返回 user_id，失败返回 401。
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    user_id = validate_user_and_get_id(username, password)
    if user_id:
        return jsonify({"message": "登录成功", "user_id": user_id})
    else:
        return jsonify({"error": "用户名或密码错误"}), 401
