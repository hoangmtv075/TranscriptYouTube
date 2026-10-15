# Transcript-YouTube

A small web service that runs on your own computer: send it a YouTube link and it returns the video's **transcript**.

Built with **Python**, **FastAPI** and **Uvicorn**. Once started, it listens at `http://127.0.0.1:8000` (also reachable as `http://localhost:8000`).

## Features

- Fetch the transcript of a YouTube video from its URL.
- Optional **timestamps** (`timestamp`).
- Optional **sentence merging**, which joins transcript fragments into complete sentences (`mergeSentences`).
- Built-in Swagger interface at `/docs` for trying the API with no extra tools.

## Requirements

- **Python 3.9 or newer**
- An internet connection (to install libraries and fetch transcripts)
- A terminal: Terminal on macOS, or PowerShell / Command Prompt on Windows

> No programming experience is required. Follow the steps in order, typing one command at a time and pressing Enter after each.

## Quick Overview

Setup takes five stages on either operating system:

| # | Stage | What it does |
|---|-------|--------------|
| 1 | Check Python | Confirms Python 3.9 or newer is installed. |
| 2 | Open the project folder | Moves your terminal into the `Transcript-YouTube` directory. |
| 3 | Create a virtual environment | Creates an isolated space (`venv`) so the project's libraries do not affect the rest of your computer. |
| 4 | Install libraries | Installs everything listed in `requirements.txt`. |
| 5 | Start the server | Runs the API on port 8000. |

First, download the project:

```bash
git clone https://github.com/YOUR-USERNAME/Transcript-YouTube.git
cd Transcript-YouTube
```

(Replace `YOUR-USERNAME` with the GitHub account that hosts the project. If you received the project as a zip file, unzip it and open that folder instead.)

---

## Part 1: macOS

### Step 1. Check Python

Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter) and run:

```bash
python3 --version
```

- If it prints `Python 3.x.x` and the version is **3.9 or higher**, continue to Step 2.
- If you see an error, or a dialog asks you to install the Command Line Tools, click **Install**, wait for it to finish, then run the command again.

Alternatively, install Python with Homebrew:

```bash
brew install python
```

Or download the official installer from <https://www.python.org/downloads/macos/>, run it, then reopen Terminal and repeat the version check.

### Step 2. Go to the project folder

```bash
cd ~/path/to/Transcript-YouTube
ls
```

Replace `~/path/to/Transcript-YouTube` with the real location of the folder. You should see `main.py` and `requirements.txt` in the list.

> Tip: type `cd ` (with a trailing space) in Terminal, then drag the project folder from Finder into the Terminal window and press Enter.

### Step 3. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your prompt starts with `(venv)`. You only need to create the environment once, but you must activate it every time you open a new Terminal window.

### Step 4. Install the libraries

```bash
pip install -r requirements.txt
```

Wait until the installation finishes without errors. This can take a minute or two.

### Step 5. Start the server

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

- When you see `Uvicorn running on http://127.0.0.1:8000`, the server is live.
- **Keep this Terminal window open.** Closing it shuts the server down.
- Open <http://localhost:8000/docs> in your browser to try the API right away.

### Running it again later (macOS)

**A. The server is not running (fresh start):**

```bash
cd ~/path/to/Transcript-YouTube
source venv/bin/activate
python -m uvicorn main:app --port 8000
```

**B. The server is already running and you want to restart it:**

1. Click the Terminal window that is running the server.
2. Press `Control + C` to stop it.
3. Run:
   ```bash
   source venv/bin/activate
   python -m uvicorn main:app --port 8000
   ```

**C. You edited `requirements.txt`:** reinstall the libraries before starting again.

```bash
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

> If you are still in the same Terminal window after pressing `Control + C`, you are already inside the project folder and the environment is still active, so the `cd` and `source` lines can be skipped. In a brand-new Terminal window, always run them first.

---

## Part 2: Windows 10 / 11

You can use either **PowerShell** or **Command Prompt (cmd)**. The steps are the same except for activating the virtual environment (Step 3). Press the Windows key, type "PowerShell" or "cmd", and press Enter to open one.

### Step 1. Check Python

```powershell
python --version
```

(You can also try `py --version`.)

- If it prints `Python 3.x.x` with version **3.9 or higher**, continue to Step 2.
- If you get an error, or Windows opens the Microsoft Store, Python is not installed correctly.

**To install Python:**

1. Download the installer from <https://www.python.org/downloads/windows/>.
2. Run it. On the first screen, tick **"Add python.exe to PATH"** *before* clicking **Install Now**.
3. When it finishes, close and reopen PowerShell or cmd, then run `python --version` again.

> Forgetting to tick "Add python.exe to PATH" is the most common cause of "python is not recognized" errors. If that happens, re-run the installer, choose **Modify** or **Repair**, and enable the option, or uninstall and reinstall.

### Step 2. Go to the project folder

```powershell
cd C:\path\to\Transcript-YouTube
dir
```

Replace the path with the real location of the folder. You should see `main.py` and `requirements.txt`. If the folder is on a different drive (for example `D:`), switch drive first in cmd by typing `D:`, or use `cd /d D:\path\to\Transcript-YouTube`.

> Tip: in File Explorer, open the project folder, click the address bar, type `powershell` (or `cmd`), and press Enter. A terminal opens already inside that folder.

### Step 3. Create and activate a virtual environment

Create the environment (same in both shells):

```powershell
python -m venv venv
```

Then activate it. **Run only the command that matches your shell:**

| Shell | Activation command |
|-------|--------------------|
| PowerShell | `venv\Scripts\Activate.ps1` |
| Command Prompt (cmd) | `venv\Scripts\activate.bat` |

After activation, your prompt starts with `(venv)`.

> **PowerShell error "running scripts is disabled on this system"?** Run the following once, answer `Y` if asked, then try activating again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Or simply use Command Prompt (cmd) with `activate.bat`, which has no such restriction.

### Step 4. Install the libraries

```powershell
pip install -r requirements.txt
```

Wait until it finishes without errors.

### Step 5. Start the server

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

- When you see `Uvicorn running on http://127.0.0.1:8000`, the server is live.
- **Keep this window open.** Closing it stops the server.
- Open <http://localhost:8000/docs> in your browser to test with the built-in Swagger interface.
- If Windows Defender Firewall asks whether to allow Python, you can click **Cancel** or allow it on **Private** networks. Because the server only listens on `127.0.0.1`, it is reachable only from your own computer.

### Running it again later (Windows)

**A. The server is not running (fresh start):**

```powershell
cd C:\path\to\Transcript-YouTube
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate.bat      # cmd
python -m uvicorn main:app --port 8000
```

**B. The server is already running and you want to restart it:** click the terminal window running the server and press `Ctrl + C` to stop it (press it twice if it does not stop). Then activate the environment and run the `python -m uvicorn ...` command again, as above.

**C. You edited `requirements.txt`:** reinstall the libraries before starting again.

```powershell
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate.bat      # cmd
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

> Run only the activation line for your own shell, not both. Text after `#` is a label, so do not type it.

---

## Part 3: Using the API

The server must be running first. These options work on both macOS and Windows, except where noted.

### Option 1: Swagger interface (easiest)

Open <http://localhost:8000/docs> in any browser. Expand the transcript endpoint, click **Try it out**, edit the JSON, and click **Execute**.

### Option 2: Postman

1. Open Postman and click **Import** (or press `Cmd/Ctrl + O`).
2. Choose the **Raw text** tab and paste the `curl` command below.
3. Click **Continue**, then **Import**, then **Send**.

```bash
curl -X POST http://localhost:8000/api/transcript \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "timestamp": true, "mergeSentences": true}'
```

Or build the request by hand: set the method to **POST**, the URL to `http://localhost:8000/api/transcript`, then open **Body**, select **raw** and **JSON**, and paste:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "timestamp": true,
  "mergeSentences": true
}
```

### Request fields

| Field | Type | Meaning |
|-------|------|---------|
| `url` | text | The full YouTube video link. |
| `timestamp` | `true` / `false` | Include timestamps with the transcript. |
| `mergeSentences` | `true` / `false` | Join transcript fragments into complete sentences. |

### Option 3: curl in a terminal

**macOS (Terminal):** use the same command as above. Single quotes around the JSON work in zsh/bash.

**Windows (Command Prompt):** cmd does not accept single quotes, so wrap the JSON in double quotes and escape the inner ones:

```bat
curl -X POST http://localhost:8000/api/transcript ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\", ^
  \"timestamp\": true, \"mergeSentences\": true}"
```

The `^` at the end of a line tells cmd the command continues on the next line. It must be the very last character on the line (no trailing spaces).

> **PowerShell:** `curl` is an alias for a different command (`Invoke-WebRequest`) and will fail with these options. Type `curl.exe` instead, and prefer Swagger or Postman for JSON bodies, since PowerShell quoting is tricky.

### Option 4: Browser

Open <http://localhost:8000/> to see the server's root page. Use `/docs` for the interactive API tester.

---

## Troubleshooting

| Problem | Likely cause and fix |
|---------|----------------------|
| `python3` / `python`: command not found (or "not recognized") | Python is missing or not on PATH. Install it (see Step 1 for your OS). On Windows, reinstall with **Add python.exe to PATH** ticked and reopen the terminal. |
| No `(venv)` at the start of the prompt | The environment is not active. Run the activation command for your OS and shell again. |
| `No module named uvicorn` / `fastapi` | Libraries are not installed in the active environment. Activate `venv`, then run `pip install -r requirements.txt`. |
| `Could not open requirements file` / `Error loading ASGI app` | You are in the wrong folder. Use `cd` to enter the project folder that contains `main.py` and `requirements.txt`. |
| `Address already in use` (port 8000) | Another program (or an old server) is using port 8000. Stop the old server with `Control/Ctrl + C`, or start on another port, e.g. `--port 8001`, and use that port in all URLs. |
| Windows: `running scripts is disabled` | In PowerShell run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or use Command Prompt with `activate.bat`. |
| Browser cannot connect to `localhost:8000` | The server is not running or its terminal was closed. Start it again and wait for the "Uvicorn running" message. |
| Transcript request returns an error | The video may have no captions, be private or age-restricted, or the link may be wrong. Try another public video that has captions. |

## Quick Command Reference

| Task | macOS | Windows |
|------|-------|---------|
| Check Python | `python3 --version` | `python --version` |
| Create environment | `python3 -m venv venv` | `python -m venv venv` |
| Activate environment | `source venv/bin/activate` | PowerShell: `venv\Scripts\Activate.ps1`<br>cmd: `venv\Scripts\activate.bat` |
| Install libraries | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Start server | `python -m uvicorn main:app --port 8000` | `python -m uvicorn main:app --port 8000` |
| Stop server | `Control + C` | `Ctrl + C` |
| Leave environment | `deactivate` | `deactivate` |

## Project Structure

```
Transcript-YouTube/
├── main.py             # Main server code (FastAPI)
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
└── README.md           # This guide
```

## Contributing

Contributions are welcome. Please open an **Issue** or submit a **Pull Request**.

## License

Released under the [MIT License](LICENSE).
