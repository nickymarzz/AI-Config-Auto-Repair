# Final Project Report: AI Config Auto-Repair Manager

## Executive Summary
The **AI Config Auto-Repair Manager** is an automated system designed to maintain the integrity of JSON configuration files. By integrating real-time file monitoring with local Large Language Model (LLM) reasoning, the system detects syntax errors instantly and proposes intelligent corrections while keeping the user in control through a "Human-in-the-loop" approval process.

---

## 🏗️ System Architecture
The project follows an **Agentic Workflow** composed of three distinct layers:

1.  **Perception Layer (File Monitoring)**:
    - Utilizes the `watchdog` library to monitor the local filesystem.
    - Specifically watches for `on_modified` events on targeted configuration files (e.g., `config.json`).
2.  **Reasoning Layer (Validation & AI)**:
    - **Validation**: Every file change is first validated using standard Python `json.loads()`.
    - **Error Analysis**: If validation fails, the `JSONDecodeError` message is captured to provide context for the AI.
    - **AI Repair**: The system communicates with a local **Llama-3** instance via the **Ollama** API. It passes the broken content and the specific error message to generate a fix.
3.  **Action Layer (Human-in-the-loop)**:
    - Instead of automatically overwriting files, the system displays a "Proposed Fix".
    - The user must explicitly approve the fix (`Y/n`) before the file is updated.
    - **Advanced Error Handling**: If the AI's response is still invalid, the system automatically retries (up to 3 attempts) to refine the output.

---

## 📝 AI Prompt Engineering
To ensure high-quality and parseable responses, a tiered prompting strategy was used:

### System Prompt
> "You are an expert, automated JSON configuration repair agent. Your job is to fix syntax errors in JSON files (missing commas, brackets, etc.) and return ONLY the valid JSON content.
> 
> **STRICT RULES:**
> 1. Return ONLY the raw, corrected JSON code.
> 2. Do NOT include any conversational text, explanations, or headers.
> 3. Do NOT use markdown formatting blocks (e.g., no \` \` \`json).
> 4. Ensure the output is immediately parseable by a standard JSON library."

### User Prompt
> "Broken JSON:
> {broken_content}
> 
> Error Message:
> {error_msg}"

The inclusion of the **Error Message** was a critical design choice, as it helps the model pinpoint exactly where the syntax failure occurred (e.g., "Expecting ',' delimiter: line 4 column 5").

---

## 🔐 The Local LLM Decision
A core requirement of this project was the use of a **Local LLM (Llama-3 via Ollama)** rather than a cloud-based API. This decision was driven by two primary factors:

1.  **Maximum Data Privacy**: Configuration files are the "heart" of most applications and often contain sensitive data (database credentials, API keys, internal paths). By using a local model, **zero data leaves the user's machine**, ensuring compliance with strict security policies.
2.  **Zero API Costs**: Traditional LLM APIs charge per token, which can become expensive for continuous monitoring tasks. Our architecture offers a **one-time hardware investment** with zero ongoing costs, making it a sustainable solution for high-frequency use.

---

## 🚧 Challenges Faced & Solutions

| Challenge | Impact | Solution |
| :--- | :--- | :--- |
| **Markdown Hallucination** | The AI often wraps code in \` \` \`json blocks, which breaks the `json.loads()` parser. | Strict system instructions and a `.strip()` operation on the response. |
| **Invalid Retries** | Sometimes the AI fixes one error but introduces another. | Implemented a **Retry Loop** (3 attempts) that provides the new error message back to the AI for refinement. |
| **Concurrency** | Frequent saves could trigger multiple AI requests simultaneously. | Used a simple synchronous processing lock within the `FileSystemEventHandler`. |
| **Hardware Overhead** | Running Llama-3 requires significant RAM/VRAM. | Optimized the setup instructions to recommend specific versions of Llama-3 (8B) that balance performance and speed on consumer hardware. |

---

## 🏁 Conclusion
The AI Config Auto-Repair Manager demonstrates that LLMs can be successfully integrated into developer workflows as reliable "auto-correct" tools. By combining local execution for privacy with a robust validation-and-retry logic, we have created a tool that is both powerful and safe for production environments.
