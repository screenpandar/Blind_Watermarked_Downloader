## 基于图文盲水印的数据中心溯源系统

这是一个用于**带水印可追溯下载**的轻量级数据中心示例项目。

> 本项目主要用于 **学习与研究/演示**，安全模型做了大量简化，**不建议直接用于生产环境**。

---

## 快速开始

### 1. 克隆项目并进入目录

```bash
git clone <your-repo-url>.git
cd Blind_watermarked_downloader
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

> 推荐使用 Python 3.8–3.11，其他版本未系统测试。

### 3. 准备数据目录

确保以下目录存在（部分会在运行时自动创建）：

- `files/`：放置服务器要提供下载的原始文件（示例中包含若干 txt 文本）。
- `downloads/`：客户端下载后的文件保存目录。
- `logs/`：存放访问日志 `access.log`。
- `exports/`：存放导出的下载日志 CSV（由 `export_logs.py` 创建）。

### 4. 初始化数据库

项目首次运行时，`app.py` 中的 `init_db()` 会自动创建 SQLite 数据库和所需表结构，如果你想**重新初始化**数据库，只需：

- **删除同目录下的 `data_center.db` 文件**，重新运行服务端即可自动重建。

### 5. 启动与基础使用

1. **启动服务端（Flask API）**

   ```bash
   python app.py
   ```

   - 默认监听 `0.0.0.0:5000`。
   - 可在 `config.py` 中调整数据库文件名、上传目录等配置。

2. **启动桌面客户端**

   ```bash
   python client.py
   ```

   - 默认服务端地址为：`http://localhost:5000`（在 `client.py` 中通过 `SERVER_URL` 配置）。
   - 如需跨机器访问，可将 `SERVER_URL` 修改为对应服务器 IP 和端口，例如：  
     `SERVER_URL = "http://192.168.1.100:5000"`。

3. **基本使用流程**

   - 在客户端注册新用户或使用已有账号登录（用户名 + 密码）；
   - 登录成功后点击“查询文件目录”，在列表中选择要下载的文件；
   - 点击“下载选中文件”，后端会根据文件类型选择文本/图像水印模块嵌入 `user_id`，将带水印文件返回并保存在 `downloads/` 目录；
   - 每次下载会在 SQLite 的 `download_logs` 表与 `logs/access.log` 中记录一条日志。

### 6. 文件目录快速对照

- **服务器侧可下载文件目录**：`files/`
- **客户端下载保存目录**：`downloads/`
- **导出的下载日志目录**：`exports/`
- **访问日志文件**：`logs/access.log`

---
## 水印提取与日志导出

### 图形化水印提取工具

```bash
python extract_watermark.py
```

- 通过 GUI 选择带水印的**文本或图片文件**。
- 自动识别文件类型并调用对应提取逻辑。
- 提取成功后会弹窗显示恢复出的 `user_id`。

### 导出下载日志为 CSV

```bash
python export_logs.py
```

- 会在 `exports/` 目录下生成形如 `download_logs_YYYYMMDD_HHMMSS.csv` 的文件。
- CSV 中包含字段：`ID, User ID, Filename, Timestamp, IP`。

---

## 安全性与注意事项

- 本项目主要用于 **学习与演示**，很多地方为方便说明而简化实现，**请勿直接用于生产环境**：
  - 密码明文存储，仅用于 Demo，不适合真实用户系统。
  - 未做严格的权限系统与限流/防重放等安全防护。
  - 文本/图片水印方案更适合做“弱防护 + 可追踪”场景，而非强 DRM。
- 如希望基于本项目演进为实际生产环境，请至少：
  - 引入密码哈希（如 `bcrypt` / `pbkdf2` 等）。
  - 增加鉴权/鉴权中间件、接口访问控制和防刷机制。
  - 对数据库和日志等敏感数据做好访问控制与备份。

---
## 功能特性

- **用户管理**
  - 用户注册（生成唯一 `user_id`，存入 SQLite 数据库）。
  - 通过用户名 + 密码进行登录校验。

- **文件下载与目录浏览**
  - 后端从 `files/` 目录提供可下载文件。
  - `/file/list` 接口列出当前可下载文件列表。
  - 客户端支持登录后在图形界面中浏览文件列表、选择文件并一键下载，下载结果保存在 `downloads/` 目录。

- **文本水印（`watermark/watermark_text.py`）**
  - 将整型 `user_id` 转为二进制串。
  - 通过在文本每行末尾追加**空格/Tab** 来编码 `0/1` 位，实现不可见水印。
  - 提供水印提取逻辑，可从被标记的文本恢复出 `user_id`。

- **图像水印（`watermark/watermark_image.py`）**
  - 基于 `blind_watermark.WaterMark` 对图片嵌入不可见字符串水印（`user_id`）。
  - 支持 PNG/JPG/JPEG/BMP 等常见图片格式。
  - 提供水印提取接口，可从图像中恢复 `user_id`。

- **下载审计 & 日志记录**
  - 每次下载会记录：`user_id`、用户名、文件名、时间戳、IP。
  - 采用 SQLite 表 `download_logs` 保存，便于后续统计与追溯。
  - 同时在 `logs/access.log` 中追加文本日志。

- **辅助工具**
  - `extract_watermark.py`：图形化水印提取工具（支持文本 + 图片）。
  - `export_logs.py`：将下载日志导出为 `exports/` 下的 CSV 文件，方便数据分析。

---

## 目录结构（简要）

```text
app.py                 # Flask 入口，注册蓝图并初始化数据库
client.py              # 桌面客户端：登录/注册用户、浏览文件列表并下载文件
config.py              # 全局配置（数据库位置、文件目录、日志路径等）
models/
  database.py          # SQLite 连接和表结构初始化
routes/
  user_routes.py       # /user/register 用户注册接口
  file_routes.py       # /file/get 文件下载 + 水印嵌入；/file/list 文件列表
services/
  user_service.py      # 用户注册、登录校验等逻辑
  file_service.py      # 下载日志写入（文件 + 数据库）
watermark/
  watermark_text.py    # 文本水印嵌入与提取
  watermark_image.py   # 图像水印嵌入与提取
extract_watermark.py   # 水印提取 GUI 工具
export_logs.py         # 将下载日志导出为 CSV
files/                 # 服务器侧可下载文件目录
downloads/             # 客户端下载保存目录
logs/
  access.log           # 文本下载日志
.env                   # 可选：环境变量（如果有使用）
README.md              # 英文说明
readme_cn.md           # 本文件（中文说明）
```

---





## 开源协议

本仓库已在根目录提供 `LICENSE` 文件，采用 **MIT License** 开源协议。

- 你可以自由学习、修改与分发本项目；
- 使用或再发布时，请保留原作者的版权声明。
