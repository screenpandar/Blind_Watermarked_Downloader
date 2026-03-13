# Blind Watermarked Downloader

A lightweight **traceable download** demo with blind watermarking for text and images.  
Flask API + desktop client + SQLite + blind watermark.

> This project is for **research and educational purposes only** and is **not production‑ready**  
> (plain-text passwords, simplified security model, no rate limiting).

---

## Quick start

```bash
git clone <https://github.com/screenpandar/Blind_Watermarked_Downloader>.git
cd Blind_watermarked_downloader
pip install -r requirements.txt
python app.py          # start server (default 0.0.0.0:5000)
python client.py       # start desktop client (default http://localhost:5000)
```

Optional: copy `.env.example` to `.env` and set `SECRET_KEY`, `DATABASE` if needed.

### Quick demo flow

1. Start the Flask server with `python app.py`.
2. Start the desktop client with `python client.py`.
3. In the client, register a new user or log in with an existing username/password.
4. After login, click “Query file list”, select a file from the list, and click “Download selected file”.  
   The server will embed the user ID as an invisible watermark into the text/image and:
   - return the watermarked file to the client (saved under `downloads/`),
   - log the download into SQLite and `logs/access.log`.

---

## Requirements

- Python **3.8–3.11** (tested; other versions may work but are not fully verified)
- OS with Tkinter support (Windows / Linux / macOS)
- See `requirements.txt` for full Python dependencies.

---

## Overview

- **Server**: user registration, file list, watermarked file download, download logging.
- **Client**: desktop GUI to register, browse files, and download (watermark auto-embedded).
- **Watermark**: text (line-end spaces/tabs) and image (blind-watermark) for user ID tracing.
- **Tools**: watermark extractor GUI and CSV export for download logs.

Suitable for learning **Flask + Tkinter + SQLite + digital watermarking** or as a base for internal content distribution and audit.

---

## Documentation

- **中文说明**：见 [readme_cn.md](readme_cn.md)（功能、目录结构、安全与开源协议说明）。

---

## Security & scope

- Uses **plain-text password storage** and simplified auth logic.
- No rate limiting, no production-grade permission system.
- Text/image watermarking is designed for **traceability demos**, not strong DRM.

Do not deploy this repository directly to production without adding proper security hardening.

---

## License

This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for details.
