# Security Policy

We take the security of AI Config Auto-Repair Manager seriously. This document outlines our policy regarding reporting security vulnerabilities and general security practices for using this tool.

## Supported Versions

Only the latest version of the repository is actively supported with security updates.

| Version | Supported |
| ------- | --------- |
| Main    | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability (such as credential leakage, prompt injection risks, or unauthorized file access), please do **not** report it via a public issue.

Instead, report it by emailing the maintainers directly or opening a private security advisory if available on the repository platform.

Please include:

* A detailed description of the vulnerability.
* Steps to reproduce the issue (proof-of-concept code or configuration).
* The potential impact of the vulnerability.

We will acknowledge receipt of your report within 48 hours and work with you to coordinate a security fix.

## 🔐 Security Best Practices

When using the AI Config Auto-Repair Manager, please adhere to the following best practices:

### 1. Protect Your Secrets

* **Never commit `.env` files** to version control. The `.gitignore` is pre-configured to ignore `.env`, but always double-check before pushing.
* If your Telegram Bot Token or OpenRouter API key is accidentally committed, **revoke it immediately** through BotFather / OpenRouter dashboard.

### 2. Limit Bot Access

* Set your `TELEGRAM_CHAT_ID` correctly to ensure the bot only interacts with *your* chat.
* Implement verification in your bot commands/polling (the watchdog script compares incoming updates against your configured `TELEGRAM_CHAT_ID` to prevent third-party command execution).

### 3. LLM Prompt Injection & AST Execution

* This tool uses AI models to generate fixes for config files. While the output is validated using `json.loads()`, caution should be exercised when allowing the AI to generate complex configurations that might contain executable strings or dynamic fields if parsed downstream by other applications.
* The Human-in-the-Loop approval mechanism (`YES` / `NO` confirmation via Telegram) is a vital layer of security. **Always review the proposed JSON diff carefully on your Telegram app before replying `YES`.**
