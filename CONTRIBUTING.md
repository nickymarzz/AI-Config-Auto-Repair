# Contributing to AI Config Auto-Repair Manager

First off, thank you for considering contributing to the AI Config Auto-Repair Manager! It is people like you who make this tool better for everyone.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in our community.

---

## 🚀 How Can I Contribute?

### Reporting Bugs

If you find a bug (e.g., the parser fails to extract JSON from a new AI model's response, or the watchdog crashes on specific filesystem events), please open an Issue. Include:

- A clear description of the bug.
- Steps to reproduce.
- Relevant system logs or error messages (redacting any API keys or private Telegram chat IDs).

### Suggesting Enhancements

We are always looking to improve the auto-repair flow. If you want to propose a new feature (e.g., supporting discord notifications, adding formatting options like black, or supporting YAML files):

- Open an Issue describing your proposal and its benefits.
- If you'd like to implement it yourself, mention it in the issue so we can coordinate!

### Pull Requests

1. **Fork the repo** and create your branch from `main`.
2. If you've added code that should be tested, add tests or describe your validation.
3. Ensure the code is properly formatted (PEP 8 guidelines for Python).
4. Update the documentation (`README.md`, `FINAL_REPORT.md`) if your changes introduce new configurations or behaviors.

---

## 🛠️ Development Setup

To set up a local development environment:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/AI-Config-Auto-Repair.git
   cd AI-Config-Auto-Repair
   ```

2. **Set up virtual environment**:

   ```powershell
   python -m venv envs/my_env3
   .\envs\my_env3\Scripts\activate
   pip install watchdog python-dotenv requests
   ```

3. **Set up your local credentials**:
   Copy `.env.example` to `.env` and fill in:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `OPENROUTER_API_KEY`

4. **Run the tool**:

   ```powershell
   python ai_auto_repair.py
   ```

---

## 🧪 Testing and Verification

Before submitting a Pull Request, verify your changes manually:

1. Run `python ai_auto_repair.py`.
2. Intentionally introduce a syntax error in `config.json` (e.g., remove a trailing comma).
3. Ensure:
   - The watchdog captures the modification.
   - The OpenRouter API is invoked with correct prompts.
   - The Telegram bot sends a message detailing the error and fix.
   - Replying `YES` applies the fix correctly.
   - Replying `NO` rejects the fix and keeps the invalid config file (or restores it).

---

## 🎨 Style Guide

- Follow **PEP 8** style guidelines for Python code.
- Write clear, concise docstrings and comment blocks explaining reasoning.
- Keep system logic separated:
  - Perception (Watchdog / Telegram polling)
  - Reasoning (LLM Prompting / Parsing)
  - Action (File IO / Alerting)
