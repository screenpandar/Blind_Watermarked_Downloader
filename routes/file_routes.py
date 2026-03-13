from flask import Blueprint, request, send_file, jsonify
from services.file_service import log_request, log_download
from services.user_service import validate_user_and_get_id
import os
from config import Config
from watermark.watermark_text import apply_text_watermark
from watermark.watermark_image import apply_image_watermark
import shutil
import tempfile

file_bp = Blueprint('file_bp', __name__)

#文件下载接口
@file_bp.route('/get', methods=['POST'])
def file_get():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    filename = data.get('filename')
    ip = request.remote_addr

    user_id = validate_user_and_get_id(username, password)
    if not user_id:
        return jsonify({"error": "用户验证失败"}), 403

    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found!"}), 404

    # 准备 temp 文件夹与水印输出
    os.makedirs('temp', exist_ok=True)
    output_path = os.path.join('temp', f"{username}_{filename}")

    try:
        # 创建临时输出文件
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, filename)

        if filename.endswith('.txt'):
            apply_text_watermark(file_path, output_path, int(user_id))
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            apply_image_watermark(file_path, output_path, int(user_id))
        else:
            return jsonify({'error': '暂不支持该类型文件'}), 400

        # 写日志
        ip = request.remote_addr
        log_request(user_id, username, filename, ip)
        log_download(user_id, username, filename, ip)
        # 使用 send_file 发送临时水印文件
        response = send_file(output_path, as_attachment=True)
        # 清理临时文件
        @response.call_on_close
        def cleanup():
            try:
                shutil.rmtree(temp_dir)
                print(f"[清理] 删除临时目录：{temp_dir}")
            except Exception as e:
                print(f"[错误] 删除临时目录失败: {e}")
        return response

    except Exception as e:
        return jsonify({'error': f'水印处理失败: {str(e)}'}), 500

#查看文件接口
@file_bp.route('/list', methods=['GET'])
def file_list():
    files = os.listdir('files')
    return jsonify({"files": files})

