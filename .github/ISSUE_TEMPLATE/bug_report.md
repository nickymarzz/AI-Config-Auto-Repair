---
name: 🐛 Bug Report
about: File a bug report to help us improve the AI Config Auto-Repair Manager.
title: '[BUG] '
labels: bug
assignees: ''
---

## 📝 Describe the Bug

A clear and concise description of what the bug is.

## 🚶 Steps to Reproduce

Steps to reproduce the behavior:

1. Start the watchdog script via `python ai_auto_repair.py`
2. Modify `config.json` with [specify invalid JSON structure]
3. Observe error / failure [e.g. script crashes, Telegram message not sent, incorrect AI correction]

## 🎯 Expected Behavior

A clear and concise description of what you expected to happen.

## 📄 Logs / Console Output

If applicable, add console output or system logs to help explain your problem.
> [!WARNING]
> Please ensure you redact any sensitive information (e.g., `TELEGRAM_BOT_TOKEN`, `OPENROUTER_API_KEY`, or private chat IDs) from your logs before posting!

```text
// Paste log output here
```

## 💻 Environment Context

- **OS**: [e.g., Windows 11, macOS, Linux]
- **Python Version**: [e.g., 3.10.5]
- **Selected AI Model**: [e.g., `openrouter/free`, `google/gemini-2.5-flash:free`]
- **Watchdog Version**: [e.g., `4.0.0`]
