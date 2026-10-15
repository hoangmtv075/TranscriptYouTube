# Transcript-YouTube

Dịch vụ web nhỏ chạy ngay trên máy của bạn: gửi vào một đường dẫn YouTube, nhận lại **bản chép lời (transcript)** của video.

Xây dựng bằng **Python**, **FastAPI** và **Uvicorn**. Sau khi chạy, server lắng nghe tại `http://127.0.0.1:8000` (hay `http://localhost:8000`).

## ✨ Tính năng

- Lấy transcript của video YouTube từ một đường link.
- Tùy chọn kèm **mốc thời gian** (`timestamp`).
- Tùy chọn **gộp các đoạn rời thành câu hoàn chỉnh** (`mergeSentences`).
- Có sẵn giao diện thử API (Swagger) tại `/docs`, không cần cài thêm công cụ.

## 📋 Yêu cầu

- **Python 3.9 trở lên**
- Kết nối Internet (để cài thư viện và lấy transcript)
- Một cửa sổ dòng lệnh: Terminal (macOS) hoặc PowerShell / Command Prompt (Windows)

> Không cần biết lập trình. Chỉ cần làm theo từng bước, gõ từng lệnh rồi nhấn Enter.

## 🚀 Cài đặt nhanh

Quá trình gồm 5 bước giống nhau trên cả hai hệ điều hành:

| # | Bước | Mục đích |
|---|------|----------|
| 1 | Kiểm tra Python | Đảm bảo đã có Python 3.9+ |
| 2 | Vào thư mục dự án | Chuyển terminal vào thư mục `Transcript-YouTube` |
| 3 | Tạo môi trường ảo (`venv`) | Cô lập thư viện của dự án, không ảnh hưởng phần còn lại của máy |
| 4 | Cài thư viện | Cài mọi thứ trong `requirements.txt` |
| 5 | Chạy server | Khởi động API ở cổng 8000 |

Trước tiên, tải mã nguồn về:

```bash
git clone https://github.com/TEN-CUA-BAN/Transcript-YouTube.git
cd Transcript-YouTube
```

(Thay `TEN-CUA-BAN` bằng tên tài khoản GitHub của bạn. Nếu bạn nhận thư mục dưới dạng file nén, hãy giải nén rồi vào thư mục đó.)

---

## 🍎 Hướng dẫn cho macOS

### Bước 1. Kiểm tra Python

Mở **Terminal** (nhấn `Cmd + Space`, gõ `Terminal`, nhấn Enter) và chạy:

```bash
python3 --version
```

- Nếu hiện `Python 3.x.x` với phiên bản **3.9 trở lên** → sang Bước 2.
- Nếu báo lỗi, hoặc có hộp thoại yêu cầu cài *Command Line Tools* → bấm **Install**, chờ xong rồi chạy lại lệnh.

Cách khác: cài bằng Homebrew:

```bash
brew install python
```

Hoặc tải bộ cài chính thức tại <https://www.python.org/downloads/macos/>, cài xong thì mở lại Terminal và kiểm tra phiên bản lần nữa.

### Bước 2. Vào thư mục dự án

```bash
cd ~/duong/dan/den/Transcript-YouTube
ls
```

Bạn phải thấy `main.py` và `requirements.txt` trong danh sách.

> 💡 Mẹo: gõ `cd ` (có dấu cách phía sau), rồi kéo thư mục dự án từ Finder thả vào cửa sổ Terminal và nhấn Enter.

### Bước 3. Tạo và kích hoạt môi trường ảo

```bash
python3 -m venv venv
source venv/bin/activate
```

Khi thành công, dòng lệnh sẽ bắt đầu bằng `(venv)`. Môi trường chỉ cần tạo **một lần**, nhưng phải **kích hoạt lại** mỗi khi mở cửa sổ Terminal mới.

### Bước 4. Cài thư viện

```bash
pip install -r requirements.txt
```

Chờ khoảng một đến hai phút cho đến khi cài xong, không báo lỗi.

### Bước 5. Chạy server

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

- Khi thấy dòng `Uvicorn running on http://127.0.0.1:8000` nghĩa là server đã hoạt động.
- **Giữ nguyên cửa sổ Terminal.** Đóng cửa sổ là server dừng.
- Mở <http://localhost:8000/docs> trên trình duyệt để thử API ngay.

### Chạy lại những lần sau (macOS)

**A. Server chưa chạy (khởi động mới):**

```bash
cd ~/duong/dan/den/Transcript-YouTube
source venv/bin/activate
python -m uvicorn main:app --port 8000
```

**B. Server đang chạy, muốn khởi động lại:**

1. Bấm vào cửa sổ Terminal đang chạy server.
2. Nhấn `Control + C` để dừng.
3. Chạy lại:
   ```bash
   source venv/bin/activate
   python -m uvicorn main:app --port 8000
   ```

**C. Bạn đã sửa `requirements.txt`:** cài lại thư viện trước khi chạy.

```bash
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

> Nếu vẫn ở cùng cửa sổ Terminal sau khi nhấn `Control + C`, bạn vẫn đang ở trong thư mục dự án và môi trường vẫn đang bật, nên có thể bỏ qua dòng `cd` và `source`. Với cửa sổ Terminal mới, luôn chạy chúng trước.

---

## 🪟 Hướng dẫn cho Windows 10 / 11

Dùng **PowerShell** hoặc **Command Prompt (cmd)** đều được. Các bước giống nhau, chỉ khác lệnh kích hoạt môi trường ảo (Bước 3). Nhấn phím Windows, gõ `PowerShell` hoặc `cmd`, rồi Enter để mở.

### Bước 1. Kiểm tra Python

```powershell
python --version
```

(Cũng có thể thử `py --version`.)

- Hiện `Python 3.x.x` từ **3.9 trở lên** → sang Bước 2.
- Báo lỗi, hoặc Windows mở Microsoft Store → Python chưa được cài đúng.

**Cách cài Python:**

1. Tải bộ cài tại <https://www.python.org/downloads/windows/>.
2. Chạy file cài. Ở màn hình đầu tiên, **tick vào "Add python.exe to PATH"** *trước khi* bấm **Install Now**.
3. Cài xong, đóng và mở lại PowerShell/cmd, rồi chạy lại `python --version`.

> Quên tick "Add python.exe to PATH" là nguyên nhân phổ biến nhất gây lỗi *"python is not recognized"*. Khi đó hãy chạy lại bộ cài, chọn **Modify** hoặc **Repair** rồi bật tùy chọn này, hoặc gỡ và cài lại.

### Bước 2. Vào thư mục dự án

```powershell
cd C:\duong\dan\den\Transcript-YouTube
dir
```

Bạn phải thấy `main.py` và `requirements.txt`. Nếu thư mục nằm ổ đĩa khác (ví dụ `D:`), trong cmd hãy gõ `D:` trước, hoặc dùng `cd /d D:\duong\dan\den\Transcript-YouTube`.

> 💡 Mẹo: trong File Explorer, mở thư mục dự án, bấm vào thanh địa chỉ, gõ `powershell` (hoặc `cmd`) rồi Enter. Cửa sổ dòng lệnh sẽ mở sẵn ngay trong thư mục đó.

### Bước 3. Tạo và kích hoạt môi trường ảo

Tạo môi trường (giống nhau ở cả hai):

```powershell
python -m venv venv
```

Kích hoạt, **chỉ chạy lệnh đúng với cửa sổ bạn đang dùng**:

| Cửa sổ | Lệnh kích hoạt |
|--------|----------------|
| PowerShell | `venv\Scripts\Activate.ps1` |
| Command Prompt (cmd) | `venv\Scripts\activate.bat` |

Khi thành công, dòng lệnh sẽ bắt đầu bằng `(venv)`.

> **PowerShell báo lỗi "running scripts is disabled on this system"?** Chạy lệnh sau một lần (nhập `Y` nếu được hỏi) rồi kích hoạt lại:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Hoặc đơn giản là dùng Command Prompt với `activate.bat`, không bị giới hạn này.

### Bước 4. Cài thư viện

```powershell
pip install -r requirements.txt
```

### Bước 5. Chạy server

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

- Thấy `Uvicorn running on http://127.0.0.1:8000` là server đã chạy.
- **Giữ nguyên cửa sổ này.** Đóng là server dừng.
- Mở <http://localhost:8000/docs> để thử bằng giao diện Swagger.
- Nếu Windows Defender Firewall hỏi có cho phép Python không, bạn có thể bấm **Cancel** hoặc cho phép trên mạng **Private**. Vì server chỉ lắng nghe ở `127.0.0.1` nên chỉ máy của bạn truy cập được.

### Chạy lại những lần sau (Windows)

**A. Server chưa chạy (khởi động mới):**

```powershell
cd C:\duong\dan\den\Transcript-YouTube
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate.bat      # cmd
python -m uvicorn main:app --port 8000
```

**B. Server đang chạy, muốn khởi động lại:** bấm vào cửa sổ đang chạy server, nhấn `Ctrl + C` (nhấn hai lần nếu chưa dừng), sau đó kích hoạt lại môi trường và chạy lệnh `python -m uvicorn ...` như trên.

**C. Bạn đã sửa `requirements.txt`:**

```powershell
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate.bat      # cmd
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

> Chỉ chạy dòng kích hoạt phù hợp với cửa sổ của bạn, không chạy cả hai. Phần chữ trong ngoặc/sau dấu `#` chỉ là ghi chú, đừng gõ vào.

---

## 🔌 Cách sử dụng API

Server cần đang chạy. Các cách dưới đây dùng được trên cả macOS và Windows (trừ chỗ có ghi chú).

### Cách 1: Giao diện Swagger (dễ nhất)

Mở <http://localhost:8000/docs> trên trình duyệt, mở endpoint transcript, bấm **Try it out**, sửa nội dung JSON rồi bấm **Execute**.

### Cách 2: Postman

1. Mở Postman, bấm **Import** (hoặc `Cmd/Ctrl + O`).
2. Chọn tab **Raw text** và dán lệnh `curl` bên dưới.
3. Bấm **Continue** → **Import** → **Send**.

```bash
curl -X POST http://localhost:8000/api/transcript \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "timestamp": true, "mergeSentences": true}'
```

Hoặc tự tạo request: phương thức **POST**, URL `http://localhost:8000/api/transcript`, vào **Body** → chọn **raw** và **JSON**, rồi dán:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "timestamp": true,
  "mergeSentences": true
}
```

### Các trường trong request

| Trường | Kiểu | Ý nghĩa |
|--------|------|---------|
| `url` | chuỗi | Đường link đầy đủ của video YouTube |
| `timestamp` | `true` / `false` | Có kèm mốc thời gian trong transcript hay không |
| `mergeSentences` | `true` / `false` | Gộp các đoạn rời thành câu hoàn chỉnh |

### Cách 3: `curl` trong terminal

**macOS (Terminal):** dùng đúng lệnh ở Cách 2 (dấu nháy đơn quanh JSON hoạt động tốt trong zsh/bash).

**Windows (Command Prompt):** cmd không nhận dấu nháy đơn, nên đặt JSON trong dấu nháy kép và thêm `\` trước các dấu nháy kép bên trong:

```bat
curl -X POST http://localhost:8000/api/transcript ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\", ^
  \"timestamp\": true, \"mergeSentences\": true}"
```

Dấu `^` cuối dòng báo cho cmd biết lệnh còn tiếp ở dòng sau, và nó phải là ký tự cuối cùng (không có dấu cách thừa).

> **PowerShell:** `curl` là bí danh của lệnh `Invoke-WebRequest` nên các tùy chọn trên sẽ lỗi. Hãy gõ `curl.exe`, và ưu tiên dùng Swagger hoặc Postman cho nội dung JSON vì cách đặt dấu nháy trong PowerShell khá rắc rối.

### Cách 4: Trình duyệt

Mở <http://localhost:8000/> để xem trang gốc của server. Dùng `/docs` để thử API tương tác.

---

## 🛠️ Xử lý sự cố

| Vấn đề | Nguyên nhân và cách khắc phục |
|--------|-------------------------------|
| `python3` / `python`: command not found (hoặc "not recognized") | Chưa cài Python hoặc chưa thêm vào PATH. Cài lại theo Bước 1. Trên Windows, cài lại và tick **Add python.exe to PATH**, rồi mở lại terminal. |
| Không có `(venv)` đầu dòng lệnh | Môi trường ảo chưa bật. Chạy lại lệnh kích hoạt đúng với hệ điều hành và loại cửa sổ. |
| `No module named uvicorn` / `fastapi` | Thư viện chưa được cài trong môi trường đang bật. Kích hoạt `venv` rồi chạy `pip install -r requirements.txt`. |
| `Could not open requirements file` / `Error loading ASGI app` | Bạn đang ở sai thư mục. Dùng `cd` vào thư mục chứa `main.py` và `requirements.txt`. |
| `Address already in use` (cổng 8000) | Có chương trình khác (hoặc server cũ) đang dùng cổng 8000. Dừng server cũ bằng `Control/Ctrl + C`, hoặc chạy cổng khác như `--port 8001` và dùng cổng đó trong mọi URL. |
| Windows: `running scripts is disabled` | Trong PowerShell chạy `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, hoặc dùng cmd với `activate.bat`. |
| Trình duyệt không vào được `localhost:8000` | Server chưa chạy hoặc cửa sổ terminal đã bị đóng. Khởi động lại và chờ dòng "Uvicorn running". |
| Yêu cầu lấy transcript trả về lỗi | Video có thể không có phụ đề, ở chế độ riêng tư, bị giới hạn độ tuổi, hoặc link sai. Hãy thử video công khai có phụ đề khác. |

## ⌨️ Bảng lệnh nhanh

| Tác vụ | macOS | Windows |
|--------|-------|---------|
| Kiểm tra Python | `python3 --version` | `python --version` |
| Tạo môi trường | `python3 -m venv venv` | `python -m venv venv` |
| Kích hoạt môi trường | `source venv/bin/activate` | PowerShell: `venv\Scripts\Activate.ps1`<br>cmd: `venv\Scripts\activate.bat` |
| Cài thư viện | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Chạy server | `python -m uvicorn main:app --port 8000` | `python -m uvicorn main:app --port 8000` |
| Dừng server | `Control + C` | `Ctrl + C` |
| Thoát môi trường | `deactivate` | `deactivate` |

## 📁 Cấu trúc thư mục

```
Transcript-YouTube/
├── main.py             # Mã nguồn chính của server (FastAPI)
├── requirements.txt    # Danh sách thư viện cần cài
├── .gitignore          # Các file không đưa lên Git
└── README.md           # Tài liệu hướng dẫn này
```

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh. Hãy mở **Issue** hoặc gửi **Pull Request**.

## 📄 Giấy phép

Phát hành theo giấy phép [MIT](LICENSE).
