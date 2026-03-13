import os
def _int_to_bin_str(user_id: int) -> str:
    return bin(user_id)[2:]  # 去掉 '0b' 前缀

def _bin_str_to_int(bin_str: str) -> int:
    return int(bin_str, 2)

def apply_text_watermark(input_path: str, output_path: str, user_id: int):
    """在文本句尾添加空格/制表符，嵌入二进制水印"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    bin_str = _int_to_bin_str(user_id)
    if len(lines) < len(bin_str):
        raise ValueError("文本内容太短，无法嵌入完整水印")

    # 每一位嵌入到每一行结尾：0=space, 1=tab
    for i, bit in enumerate(bin_str):
        if bit == '0':
            lines[i] = lines[i].rstrip('\n') + ' \n'  # 空格 + 回车
        else:
            lines[i] = lines[i].rstrip('\n') + '\t\n'  # 制表符 + 回车

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ 水印已嵌入到：{output_path}（用户ID={user_id}）")

def extract_text_watermark(file_path: str) -> int:
    """从文本中提取隐藏的水印（用户ID）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    bin_str = ''
    for line in lines:
        if line.endswith(' \n'):
            bin_str += '0'
        elif line.endswith('\t\n'):
            bin_str += '1'
        else:
            break  # 遇到不是水印的内容就结束

    if not bin_str:
        raise ValueError("未检测到水印")

    user_id = _bin_str_to_int(bin_str)
    print(f"🕵️ 提取到的用户ID为：{user_id}")
    return user_id
