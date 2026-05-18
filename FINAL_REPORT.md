# Final Project Report: AI Config Auto-Repair Manager

## Executive Summary
The **AI Config Auto-Repair Manager** is an automated watchdog system designed to maintain the integrity of JSON configuration files. By integrating real-time file monitoring with advanced Large Language Model (LLM) reasoning via OpenRouter, the system detects syntax errors instantly, generates precise corrections, and secures human approval directly through a mobile **Telegram** interface before applying any modifications.

---

## 🏗️ System Architecture
The project follows a robust **Agentic Workflow** composed of three distinct layers:

1. **Perception Layer (File & Log Monitoring)**:
   - Utilizes the `watchdog` library to monitor the local filesystem for `on_modified` events on target configuration files (e.g., `config.json`).
   - Integrates seamlessly with OpenClaw Gateway by monitoring local Telegram session logs (`sessions.json.telegram-messages.json`) via WSL, completely avoiding Telegram Bot API `409 Conflict` errors.

2. **Reasoning Layer (Validation & AI AST Repair)**:
   - **Validation**: Every file change is validated using Python's robust `json.loads()`.
   - **Error Analysis**: If validation fails, the exact `JSONDecodeError` message and line/column offsets are captured to provide context for the AI.
   - **AI Repair**: The system communicates directly with OpenRouter's REST API (supporting models like DeepSeek Flash, Gemini 2.5 Flash, Llama 3.3, etc.). It passes the broken content and the specific error message to generate an exact drop-in replacement.

3. **Action Layer (Telegram Human-in-the-Loop)**:
   - Instead of pausing for terminal input, the system pushes a mobile alert containing the error details and the proposed fix directly to the user's Telegram app.
   - The system polls incoming Telegram messages in real time. The user simply replies **`YES`** to approve or **`NO`** to reject.
   - Upon receiving approval, the script safely overwrites the target file and sends a confirmation message back to Telegram.

---

## 📝 AI Prompt Engineering
To ensure high-quality, parseable responses from reasoning models (like DeepSeek v4 Flash), a strict, non-conversational prompting strategy was used:

### System Prompt
> "You are a JSON syntax repair assistant. When given broken JSON, return ONLY the corrected valid JSON. No explanation, no markdown."

### User Prompt
> "The following JSON file has a syntax error:
> Error: {error}
> 
> Broken JSON content:
> {broken_content}
> 
> Fix ALL syntax errors and return ONLY the corrected valid JSON."

### Robust Response Extraction
Because reasoning models often return thinking processes in `reasoning_content` and the final answer in `content` (or sometimes leave `content` null), the system implements an advanced multi-stage extraction pipeline (`extract_json_from_text`):
1. Tries raw text parsing directly.
2. Strips markdown fences (` ```json `) and re-evaluates.
3. Uses regular expressions to extract the outermost `{ ... }` object block from reasoning text as a robust fallback.

---

## 🔐 Evolution from Local LLM to OpenRouter & Telegram
The project initially explored local LLM execution (Llama-3 via Ollama) to guarantee zero data egress. However, as the architectural requirements expanded to include remote mobile approvals and multi-model flexibility, the system successfully transitioned to **OpenRouter**:

1. **Zero-Overhead REST API**: Bypassing complex agent orchestration runtimes eliminated context overflow issues and reduced system prompt token consumption by over 99%.
2. **Model Agility**: Developers can instantly switch between state-of-the-art reasoning models (`openrouter/free`, `openrouter/auto`, `google/gemini-2.5-flash:free`) by changing a single configuration line.
3. **Mobile Human-in-the-Loop**: Integrating Telegram notifications and reply polling transforms configuration management from a desktop-bound chore into an agile, on-the-go workflow.

---

## 🚧 Challenges Faced & Solutions

| Challenge | Impact | Solution |
| :--- | :--- | :--- |
| **Telegram `409 Conflict`** | OpenClaw Gateway actively polling `getUpdates` blocked the Python script from polling the same bot token. | Switched from REST polling to reading OpenClaw's local `telegram-messages.json` log file via WSL `tail`. |
| **Reasoning Model `null` Content** | Models like DeepSeek Flash return `content=null` while placing answers in `reasoning_content`. | Implemented dual-field inspection checking both `content` and `reasoning_content` with regex AST fallback extraction. |
| **Markdown Hallucination** | Models frequently wrap JSON in markdown code blocks. | Built automated regex stripping to sanitize ` ```json ` blocks before validation. |
| **Rate Limiting** | Free tier daily limits on specific models (e.g., DeepSeek free). | Documented drop-in replacements like `openrouter/auto` and `openrouter/free` to ensure uninterrupted operation. |

---

## 🏁 Conclusion
The **AI Config Auto-Repair Manager** represents a highly resilient, production-ready implementation of an agentic auto-healing workflow. By combining direct REST inference, robust AST extraction, and an elegant, conflict-free Telegram polling mechanism, the system provides an exceptionally smooth and secure developer experience.
