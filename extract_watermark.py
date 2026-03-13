import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from watermark.watermark_image import extract_image_watermark


# ---- 文本水印相关代码 ----
def _int_to_bin_str_text(user_id: int) -> str:
    return bin(user_id)[2:]  # 去掉 '0b' 前缀


def _bin_str_to_int_text(bin_str: str) -> int:
    return int(bin_str, 2)


def extract_text_watermark(file_path: str) -> int:
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

    user_id = _bin_str_to_int_text(bin_str)
    return user_id


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("水印提取工具")
    app.geometry("640x220")

    # 顶部标题
    title_label = ctk.CTkLabel(app, text="图文水印提取工具", font=ctk.CTkFont(size=22, weight="bold"))
    title_label.pack(pady=(15, 5))

    # 文件选择区域
    file_frame = ctk.CTkFrame(app)
    file_frame.pack(fill="x", padx=20, pady=(10, 5))

    file_label = ctk.CTkLabel(file_frame, text="选择图像或文本文件：")
    file_label.pack(side="left", padx=(10, 5), pady=10)

    file_path_var = ctk.StringVar(value="")

    file_entry = ctk.CTkEntry(file_frame, textvariable=file_path_var, width=360, placeholder_text="支持 .txt / .png / .jpg / .jpeg / .bmp")
    file_entry.pack(side="left", padx=(0, 5), pady=10, fill="x", expand=True)

    def browse_file():
        initial_dir = os.getcwd()
        # 使用元组形式提供多种扩展名，兼容 Windows 下的 tkinter 实现
        path = filedialog.askopenfilename(
            title="选择文件",
            initialdir=initial_dir,
            filetypes=(
                ("图片和文本文件", ("*.txt", "*.png", "*.jpg", "*.jpeg", "*.bmp")),
                ("文本文件", "*.txt"),
                ("图片文件", ("*.png", "*.jpg", "*.jpeg", "*.bmp")),
                ("所有文件", "*.*"),
            ),
        )
        if path:
            file_path_var.set(path)

    browse_button = ctk.CTkButton(file_frame, text="浏览...", width=80, command=browse_file)
    browse_button.pack(side="left", padx=(5, 10), pady=10)

    # 提取结果区域
    result_frame = ctk.CTkFrame(app)
    result_frame.pack(fill="x", padx=20, pady=(5, 5))

    result_label_title = ctk.CTkLabel(result_frame, text="提取结果：", anchor="w")
    result_label_title.pack(side="left", padx=(10, 5), pady=8)

    result_var = ctk.StringVar(value="尚未提取")
    result_value_label = ctk.CTkLabel(result_frame, textvariable=result_var, anchor="w")
    result_value_label.pack(side="left", padx=(0, 10), pady=8)

    # 底部按钮
    button_frame = ctk.CTkFrame(app)
    button_frame.pack(fill="x", padx=20, pady=(10, 15))

    def handle_extract():
        path = file_path_var.get().strip()
        if not path:
            messagebox.showwarning("警告", "请先选择文件")
            return

        try:
            if path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                user_id = extract_image_watermark(path)
            elif path.endswith('.txt'):
                user_id = extract_text_watermark(path)
            else:
                messagebox.showerror("错误", "不支持的文件格式（仅支持文本和常见图片格式）")
                return

            result_var.set(f"提取的用户ID是：{user_id}")
            messagebox.showinfo("水印提取成功", f"提取的用户ID是：{user_id}")
        except Exception as e:
            result_var.set("提取失败")
            messagebox.showerror("错误", f"提取水印失败：{e}")

    extract_button = ctk.CTkButton(button_frame, text="提取水印", command=handle_extract)
    extract_button.pack(side="right", padx=(5, 0))

    close_button = ctk.CTkButton(
        button_frame,
        text="关闭",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover=False,
        command=app.destroy,
    )
    close_button.pack(side="left", padx=(0, 5))

    app.mainloop()


if __name__ == "__main__":
    main()
