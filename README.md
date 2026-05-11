# 🤖 AI Config Auto-Repair Manager

An automated, AI-powered system that monitors JSON configuration files, detects syntax errors in real-time, and uses a local Large Language Model (Llama-3) to propose and apply fixes.

## 🌟 Features
- **Real-time Monitoring**: Uses `watchdog` to detect file saves instantly.
- **AI-Powered Repair**: Integrates with **Ollama** and **Llama-3** to intelligently fix syntax errors (missing commas, brackets, etc.).
- **Human-in-the-loop**: Never overwrites your data without permission. It shows you the proposed fix and waits for a `Y/n` confirmation.
- **Advanced Error Handling**: If the AI provides an invalid fix, the system catches the error and automatically retries.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- **Python 3.10+**
- **Ollama**: [Download here](https://ollama.com/)

### 2. Configure Ollama & Llama-3
1. Install Ollama and ensure the service is running.
2. Download the Llama-3 model by running this in your terminal:
   ```powershell
   ollama run llama3
   ```
   *(You can close the chat once the download is complete.)*

### 3. Environment Setup
Create a virtual environment and install the required libraries:
```powershell
# Create environment
python -m venv my_env
# Activate it (Windows)
.\my_env\Scripts\activate
# Install dependencies
pip install watchdog ollama
```

---

## 🚀 How to Use

1. **Start the Manager**:
   Run the main script in your terminal:
   ```powershell
   python -u ai_auto_repair.py
   ```

2. **Break a File**:
   Open `config.json` and intentionally break it (e.g., remove a comma or a closing brace) and save.

3. **Approve the Fix**:
   - The script will detect the change and identify the error.
   - It will consult Llama-3 and display a "Proposed Fix".
   - Type **`Y`** and press **Enter** to apply the fix automatically.

---

## 📂 Project Structure
- `ai_auto_repair.py`: The main integrated system (Watcher + Validator + AI).
- `config.json`: The configuration file being monitored.
- `test_llama.py`: A small utility to test your connection to the local LLM.
- `watch_script.py`: A basic file watcher implementation for testing.

---

## 🎓 Academic Note
This project demonstrates the implementation of an **Agentic Workflow**:
- **Perception**: Monitoring file system events.
- **Reasoning**: Validating data and error analysis.
- **Action**: Correcting mistakes with AI and interacting with the user.
