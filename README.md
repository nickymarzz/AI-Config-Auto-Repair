# 🤖 AI Config Auto-Repair Manager

An automated, AI-powered watchdog system that monitors JSON configuration files, detects syntax errors in real-time, and uses cutting-edge AI models via OpenRouter to propose fixes and secure human approval directly via **Telegram**.

---

## 🌟 Features
- **Real-Time Monitoring**: Uses `watchdog` to detect file saves instantly.
- **AI-Powered Repair**: Integrates directly with **OpenRouter** (supporting DeepSeek Flash, Llama 3.3, Gemini 2.5 Flash, etc.) to intelligently fix syntax errors (missing commas, brackets, extra quotes, etc.).
- **Telegram Human-in-the-Loop**: Never overwrites your data without permission. It pushes the proposed fix directly to your Telegram chat and listens for your `YES` or `NO` reply.
- **Secure Configuration**: Keeps secrets safe by loading API keys and bot tokens dynamically from `.env` files, avoiding accidental exposure.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- **Python 3.10+**
- **Telegram Bot Token & Chat ID** (to receive alerts and send approvals)
- **OpenRouter API Key** (to perform the automated AI configuration fixes)

### 2. Environment Setup
1. **Activate your environment** and install the required watchdog dependency:
   ```powershell
   # Activate your environment
   .\envs\my_env3\Scripts\activate
   # Install watchdog
   pip install watchdog
   ```

2. **Configure Credentials**:
   Copy `.env.example` to `.env` and fill in your actual credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

### 3. Configure Your AI Model
Open `ai_auto_repair.py` and set your preferred OpenRouter model via `OPENROUTER_MODEL` (defaults to `"openrouter/free"`).


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
- **Perception**: Monitoring file system events and incoming Telegram messages.
- **Reasoning**: Validating JSON data, analyzing syntax errors, and generating precise AST repairs via LLMs.
- **Action**: Pushing mobile alerts and executing human-approved file modifications.

```mermaid
graph TD
    %% Styling and Architecture Elements
    classDef client fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef monitor fill:#e3f2fd,stroke:#2196f3,stroke-width:2px;
    classDef brain fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px;
    classDef gate fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;

    %% Elements Definition
    Dev((Developer)):::client
    TargetFile[config.json File]:::client

    subgraph Local_Runtime_Agent [Perception Agent Layer]
        Watchdog Engine[Watchdog File Monitor]:::monitor
        Parser[Native JSON Validator]:::monitor
        Writer[Atomic Overwrite Engine]:::monitor
    end

    subgraph Cloud_Reasoning [AI Core Inference Layer]
        OpenRouterAPI[OpenRouter API Gateway]:::brain
        LLM[LLM Reasoning Engine]:::brain
    end

    subgraph Security_Gate [Human-In-The-Loop Validation Layer]
        TelegramBot[Telegram Bot API]:::gate
        TelegramApp[Mobile Developer Client]:::gate
    end

    %% Pipeline Processing Stream
    Dev -->|1. Saves Manual Changes| TargetFile
    TargetFile -.->|2. Asynchronous I/O Hook| Watchdog Engine
    Watchdog Engine -->|3. Traps Save Event| Parser
    
    Parser -->|Syntax Valid| Pass((Terminate Process))
    Parser -->|Syntax Invalid: Throws Exception| OpenRouterAPI
    
    OpenRouterAPI -->|4. Post Error Context| LLM
    LLM -->|5. Compiles Corrected Structural JSON| TelegramBot
    TelegramBot -->|6. Pushes Interactive Notification| TelegramApp
    
    TelegramApp -->|7. User Reviews & Sends 'YES'| Writer
    Writer -->|8. Secure Overwrite| TargetFile
```

