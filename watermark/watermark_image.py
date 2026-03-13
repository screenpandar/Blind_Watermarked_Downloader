import cv2
import numpy as np
import math
import os
from blind_watermark import WaterMark


def apply_image_watermark(input_path, output_path, user_id):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img(input_path)
    wm = str(user_id)
    bwm1.read_wm(wm, mode='str')
    bwm1.embed(output_path)
    len_wm = len(bwm1.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
    print(f"✅ 图像水印已嵌入到：{output_path}（user_id={user_id}）")

def extract_image_watermark(image_path) -> int:
    bwm1 = WaterMark(password_img=1, password_wm=1)
    len_wm = 78                #根据嵌入水印的长度调整
    user_id = bwm1.extract(image_path, wm_shape=len_wm, mode='str')
    print(f"🕵️ 提取图像水印成功：user_id = {user_id}")
    return user_id




