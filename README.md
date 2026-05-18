# 🤖 AI Config Auto-Repair Manager

An automated, AI-powered watchdog system that monitors JSON configuration files, detects syntax errors in real-time, and uses cutting-edge AI models via OpenRouter to propose fixes and secure human approval directly via **Telegram**.

---

## 🌟 Features
- **Real-Time Monitoring**: Uses `watchdog` to detect file saves instantly.
- **AI-Powered Repair**: Integrates directly with **OpenRouter** (supporting DeepSeek Flash, Llama 3.3, Gemini 2.5 Flash, etc.) to intelligently fix syntax errors (missing commas, brackets, extra quotes, etc.).
- **Telegram Human-in-the-Loop**: Never overwrites your data without permission. It pushes the proposed fix directly to your Telegram chat and listens for your `YES` or `NO` reply.
- **Conflict-Free Architecture**: Seamlessly integrates with OpenClaw Gateway by reading local Telegram message logs via WSL, completely avoiding Telegram Bot API `409 Conflict` errors.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- **Python 3.10+**
- **WSL (Windows Subsystem for Linux)** with OpenClaw Gateway configured.

### 2. Configure Your AI Model
Open `ai_auto_repair.py` and set your preferred OpenRouter model on **Line 22**:
```python
OPENROUTER_MODEL = "openrouter/free"  # Or "openrouter/auto", "google/gemini-2.5-flash:free", etc.
```

### 3. Environment Setup
Activate your Python environment and install the required library:
```powershell
# Activate your environment
.\envs\my_env3\Scripts\activate
# Install watchdog
pip install watchdog
```

---

## 🚀 How to Use

1. **Start the Watchdog**:
   Run the main script in your terminal:
   ```powershell
   & D:/PY/envs/my_env3/python.exe -u "d:/OS Agentic AI/AI-Config-Auto-Repair/ai_auto_repair.py"
   ```

2. **Break a File**:
   Open `config.json`, intentionally break the syntax (e.g., remove a comma or closing brace), and save the file.

3. **Approve on Telegram**:
   - The script instantly detects the change and identifies the error.
   - It consults OpenRouter and sends a formatted alert to your Telegram app.
   - Simply reply **`YES`** in your Telegram chat to apply the fix automatically!

---

## 📂 Project Structure
- `ai_auto_repair.py`: The main integrated watchdog system (Watcher + Validator + OpenRouter + Telegram Poller).
- `config.json`: The sample configuration file being monitored.
- `README.md`: This documentation file.
- `FINAL_REPORT.md`: Comprehensive documentation on system architecture and design decisions.

---

## 🎓 Academic Note
This project demonstrates the implementation of a state-of-the-art **Agentic Workflow**:
- **Perception**: Monitoring file system events and local Telegram logs.
- **Reasoning**: Validating JSON data, analyzing syntax errors, and generating precise AST repairs via LLMs.
- **Action**: Pushing mobile alerts and executing human-approved file modifications.
