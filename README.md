Roblox Mass Reporter TOOL :

download python previous version 3.11 or 3.12 -
not latest;

# Roblox Free Bulk Reporter

A free automated Roblox reporting tool that rotates through fresh accounts to submit reports. No paid CAPTCHA services, proxies, or API keys required.

> **Disclaimer:** Use this project responsibly and only in accordance with Roblox's Terms of Use and applicable laws.

---

# ✨ Features

- 🤖 Automatic account rotation
- 🔄 Fresh account generation
- 🛡️ Free browser-based CAPTCHA solving
- ⚡ Bulk reporting workflow
- ⏱️ Configurable delays and cooldowns
- 💸 No paid CAPTCHA services
- 🔑 No API keys required
- 🌐 Cross-platform support (Windows, Linux, macOS)

---

# 📋 Requirements

- Python 3.8+
- Google Chrome (latest)
- Windows, Linux, or macOS

---

# 🚀 Installation

## 1. Install Python

### Windows

Download Python from:

https://python.org

✔ Check **"Add Python to PATH"** during installation.

### Linux

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### macOS

```bash
brew install python3
```

---

## 2. Download the Project

```bash
git clone https://github.com/yourusername/robux-reporter-free.git

cd robux-reporter-free
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `pip` doesn't work:

### Windows

```bash
py -m pip install -r requirements.txt
```

### Linux / macOS

```bash
pip3 install -r requirements.txt
```

---

# ▶️ Run

```bash
python main.py
```

If `python` doesn't work:

### Windows

```bash
py main.py
```

### Linux / macOS

```bash
python3 main.py
```

---

# 📝 Configure Targets

Open:

```text
targets.txt
```

Add one Roblox User ID per line:

```text
123456789
987654321
555555555
```

Save the file.

Example profile URL:

```text
https://www.roblox.com/users/123456789/profile
```

User ID:

```text
123456789
```

---

# ⚙️ How It Works

1. Creates fresh Roblox accounts.
2. Warms each account by browsing Roblox.
3. Rotates between accounts.
4. Sends reports.
5. Waits using randomized delays.
6. Places accounts on cooldown.
7. Continues until all targets are processed.

---

# 🛑 Stop the Tool

```text
CTRL + C
```

---

# ❓ Troubleshooting

| Problem | Solution |
|----------|----------|
| Python not found | Use `py` or `python3` |
| Pip not found | Use `py -m pip` or `pip3` |
| Module missing | Run `pip install -r requirements.txt` |
| Chrome missing | Install the latest Chrome |
| Internet issues | Check your connection and restart |

---

# ⚙️ Configuration

Edit:

```text
config.py
```

Available settings:

- Number of accounts
- Reports per account
- Delay between actions
- Cooldown duration
- Browser settings
- Timing options

---

# 📁 Project Structure

```text
robux-reporter-free/
│
├── main.py
├── config.py
├── targets.txt
├── requirements.txt
├── modules/
├── browser/
├── utils/
└── README.md
```

---

# 💻 Supported Platforms

- ✅ Windows
- ✅ Linux
- ✅ macOS

---

# 📜 License

MIT License

See the `LICENSE` file for details.

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

