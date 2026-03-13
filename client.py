import os
import requests
import customtkinter as ctk
from tkinter import messagebox


SERVER_URL = "http://localhost:5000"
PAGE_SIZE = 50


def register_user(username: str, password: str) -> str:
    try:
        response = requests.post(f"{SERVER_URL}/user/register", json={
            "username": username,
            "password": password
        })
        data = response.json()
        # 后端返回的是 register_user 的结果字典
        if response.status_code == 200:
            return data.get("message", "注册成功")
        return data.get("error", "注册失败")
    except Exception as e:
        return f"请求失败: {e}"


def login_user(username: str, password: str):
    """
    调用后端 /user/login 接口校验用户。
    成功返回 (True, user_id, message)，失败返回 (False, None, error_msg)
    """
    try:
        response = requests.post(f"{SERVER_URL}/user/login", json={
            "username": username,
            "password": password
        })
        data = response.json()
        if response.status_code == 200:
            return True, data.get("user_id"), data.get("message", "登录成功")
        else:
            return False, None, data.get("error", "登录失败")
    except Exception as e:
        return False, None, f"请求失败: {e}"


def download_file(username: str, password: str, filename: str) -> str:
    try:
        response = requests.post(f"{SERVER_URL}/file/get", json={
            "username": username,
            "password": password,
            "filename": filename
        })

        if response.status_code == 200:
            os.makedirs("downloads", exist_ok=True)
            filepath = os.path.join("downloads", filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return f"✅ 文件下载成功，保存为: {filepath}"
        else:
            return f"❌ 下载失败: {response.json().get('error', '未知错误')}"
    except Exception as e:
        return f"请求失败: {e}"


def fetch_file_list():
    try:
        response = requests.get(f"{SERVER_URL}/file/list")
        if response.status_code == 200:
            return True, sorted(response.json().get("files", []))
        else:
            return False, []
    except Exception:
        return False, []


def create_gui():
    # 全局外观设置
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("数据中心客户端")
    app.geometry("720x520")

    # 当前登录状态
    current_user = {"username": None, "password": None, "user_id": None}

    # 三个主要界面：登录 / 注册 / 主界面（使用 pack 统一管理）
    login_frame = ctk.CTkFrame(app)
    register_frame = ctk.CTkFrame(app)
    main_frame = ctk.CTkFrame(app)

    def show_frame(frame):
        """在窗口中切换显示的主框架，避免混用不同布局管理器。"""
        for f in (login_frame, register_frame, main_frame):
            f.pack_forget()
        frame.pack(expand=True, fill="both", padx=20, pady=20)

    # ---------------- 登录界面 ----------------
    login_title = ctk.CTkLabel(login_frame, text="用户登录", font=ctk.CTkFont(size=22, weight="bold"))
    login_title.pack(pady=20)

    login_username = ctk.CTkEntry(login_frame, placeholder_text="用户名")
    login_username.pack(pady=10, ipadx=5, ipady=5)

    login_password = ctk.CTkEntry(login_frame, placeholder_text="密码", show="*")
    login_password.pack(pady=10, ipadx=5, ipady=5)

    def handle_login():
        username = login_username.get().strip()
        password = login_password.get().strip()
        if not username or not password:
            messagebox.showwarning("提示", "用户名和密码不能为空")
            return

        ok, user_id, msg = login_user(username, password)
        if ok:
            current_user["username"] = username
            current_user["password"] = password
            current_user["user_id"] = user_id
            messagebox.showinfo("登录结果", msg)
            load_user_info()
            show_frame(main_frame)
            refresh_file_list()
        else:
            messagebox.showerror("登录失败", msg)

    login_button = ctk.CTkButton(login_frame, text="登录", command=handle_login)
    login_button.pack(pady=15)

    switch_to_register = ctk.CTkButton(
        login_frame,
        text="没有账号？点击注册",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover=False,
        command=lambda: show_frame(register_frame),
    )
    switch_to_register.pack(pady=5)

    # ---------------- 注册界面 ----------------
    register_title = ctk.CTkLabel(register_frame, text="注册新用户", font=ctk.CTkFont(size=22, weight="bold"))
    register_title.pack(pady=20)

    reg_username = ctk.CTkEntry(register_frame, placeholder_text="用户名")
    reg_username.pack(pady=10, ipadx=5, ipady=5)

    reg_password = ctk.CTkEntry(register_frame, placeholder_text="密码", show="*")
    reg_password.pack(pady=10, ipadx=5, ipady=5)

    def handle_register():
        username = reg_username.get().strip()
        password = reg_password.get().strip()
        if not username or not password:
            messagebox.showwarning("提示", "用户名和密码不能为空")
            return
        msg = register_user(username, password)
        messagebox.showinfo("注册结果", msg)

    register_button = ctk.CTkButton(register_frame, text="注册", command=handle_register)
    register_button.pack(pady=15)

    switch_to_login = ctk.CTkButton(
        register_frame,
        text="已有账号？返回登录",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover=False,
        command=lambda: show_frame(login_frame),
    )
    switch_to_login.pack(pady=5)

    # ---------------- 主界面（文件列表与下载） ----------------
    header_frame = ctk.CTkFrame(main_frame)
    header_frame.pack(fill="x", pady=(10, 5), padx=10)

    user_label = ctk.CTkLabel(header_frame, text="", anchor="w")
    user_label.pack(side="left", padx=5)

    def load_user_info():
        if current_user["username"]:
            user_label.configure(text=f"当前用户：{current_user['username']}")
        else:
            user_label.configure(text="未登录")

    refresh_button = ctk.CTkButton(header_frame, text="查询文件目录", command=lambda: refresh_file_list())
    refresh_button.pack(side="right", padx=5)

    # 文件列表区域
    list_frame = ctk.CTkFrame(main_frame)
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)

    file_list_label = ctk.CTkLabel(list_frame, text="可下载文件：", anchor="w")
    file_list_label.pack(anchor="w", pady=(5, 2))

    # 高度略缩短，避免在默认窗口高度下挤压底部按钮区域
    scrollable_files = ctk.CTkScrollableFrame(list_frame, height=260)
    scrollable_files.pack(fill="both", expand=True, pady=(0, 5))

    selected_file_var = ctk.StringVar(value="")
    all_files = []
    visible_count = 0
    # 当前高亮的按钮，用于点击后切换高亮
    selected_button_ref = {"widget": None}

    def render_files():
        for widget in scrollable_files.winfo_children():
            widget.destroy()

        if not all_files:
            empty_label = ctk.CTkLabel(scrollable_files, text="暂时没有可下载的文件。")
            empty_label.pack(pady=10)
            return

        current_selected = selected_file_var.get()

        for filename in all_files[:visible_count]:
            # 使用按钮而不是单选框，点击即选中该文件，并高亮显示
            def make_on_click(name: str, button: ctk.CTkButton):
                def _on_click():
                    # 先取消之前按钮的高亮
                    if selected_button_ref["widget"] is not None:
                        selected_button_ref["widget"].configure(
                            fg_color=("gray30", "gray25"),
                            hover_color=("gray40", "gray35"),
                        )
                    # 更新当前选中文件与按钮样式
                    selected_file_var.set(name)
                    button.configure(
                        fg_color=("#1f6aa5", "#144870"),
                        hover_color=("#215f90", "#133d60"),
                    )
                    selected_button_ref["widget"] = button
                return _on_click

            # 根据当前是否选中设置初始颜色
            is_selected = filename == current_selected
            fg_color = ("#1f6aa5", "#144870") if is_selected else ("gray30", "gray25")
            hover_color = ("#215f90", "#133d60") if is_selected else ("gray40", "gray35")

            btn = ctk.CTkButton(
                scrollable_files,
                text=filename,
                anchor="w",
                fg_color=fg_color,
                hover_color=hover_color,
                command=None,  # 先创建按钮对象，再绑定回调
            )
            btn.configure(command=make_on_click(filename, btn))
            btn.pack(fill="x", padx=5, pady=2)

            # 如果是当前选中的文件，记录为高亮按钮
            if is_selected:
                selected_button_ref["widget"] = btn

    def update_show_more_button():
        remaining = max(0, len(all_files) - visible_count)
        if remaining > 0:
            show_more_button.configure(
                state="normal",
                text=f"显示更多（剩余 {remaining} 个）",
            )
        else:
            show_more_button.configure(state="disabled", text="没有更多文件了")

    def refresh_file_list():
        nonlocal all_files, visible_count
        ok, files = fetch_file_list()
        if not ok:
            messagebox.showerror("错误", "获取文件列表失败，请检查服务器是否已启动。")
            return

        all_files = files
        visible_count = min(PAGE_SIZE, len(all_files))
        render_files()
        update_show_more_button()

    def handle_show_more():
        nonlocal visible_count
        if visible_count < len(all_files):
            visible_count = min(visible_count + PAGE_SIZE, len(all_files))
            render_files()
            update_show_more_button()

    show_more_button = ctk.CTkButton(
        list_frame,
        text="显示更多",
        command=handle_show_more,
    )
    show_more_button.pack(pady=(5, 5))

    # 下载按钮
    action_frame = ctk.CTkFrame(main_frame)
    action_frame.pack(fill="x", padx=10, pady=(0, 10))

    def handle_download_selected():
        filename = selected_file_var.get()
        if not filename:
            messagebox.showwarning("提示", "请先在列表中选择要下载的文件。")
            return
        if not current_user["username"] or not current_user["password"]:
            messagebox.showwarning("提示", "请先登录。")
            return
        msg = download_file(current_user["username"], current_user["password"], filename)
        if msg.startswith("✅"):
            messagebox.showinfo("下载结果", msg)
        else:
            messagebox.showerror("下载失败", msg)

    download_button = ctk.CTkButton(action_frame, text="下载选中文件", command=handle_download_selected)
    download_button.pack(side="right", padx=5)

    back_to_login = ctk.CTkButton(
        action_frame,
        text="退出登录",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover=False,
        command=lambda: (current_user.update({"username": None, "password": None, "user_id": None}),
                         load_user_info(),
                         show_frame(login_frame)),
    )
    back_to_login.pack(side="left", padx=5)

    # 默认显示登录界面
    show_frame(login_frame)
    app.mainloop()


if __name__ == "__main__":
    create_gui()
