---
name: json-auto-repair
description: Monitors and validates JSON configuration files, identifies exact syntax errors, reports them to the user for review, and asks for explicit permission before applying any fixes.
metadata: {"requires": {"bins": ["python3"]}}
---

# JSON Auto-Repair & Human-in-the-Loop Validation

## Overview
This skill enables OpenClaw to act as an autonomous sentinel for JSON configuration files. When a JSON configuration file (such as `config.json`) is modified or when the user requests a check, OpenClaw validates the syntax, pinpoints the exact line and column of any errors, reports the details via chat, and strictly requires explicit human authorization before rewriting the file.

## When to Use
Use this skill whenever the user asks to check, verify, inspect, or repair a JSON configuration file.

## Workflows

### Step 1: Validate the JSON File via Bash Tool
**CRITICAL INSTRUCTION FOR AI AGENT:** DO NOT ask the user to paste or share the file content. You have direct filesystem and shell access. You MUST immediately invoke your bash/exec tool to run the validation script:

1. Call: `python3 {baseDir}/validate_json.py "<path_to_json_file>"`
2. Read and parse the JSON output returned by the command.

### Step 2: Handle Validation Results
- **If `status` is `valid`**: Inform the user that the JSON configuration is perfectly valid and no action is needed. Stop execution.
- **If `status` is `error`**: Proceed immediately to Step 3.

### Step 3: Report Error Location & Propose Fix
1. Analyze the error output from the script (which includes the exact `line`, `column`, and `message`).
2. Use your LLM reasoning capabilities to generate the corrected, valid JSON content.
3. **CRITICAL GUARDRAIL - DO NOT MODIFY THE FILE YET.** Send a chat message to the user containing:
   - 🚨 **Error Summary**: The exact line and column where the syntax broke (e.g., `Line X, Column Y`).
   - 🔍 **Error Details**: Description of the syntax issue (e.g., missing comma, unclosed bracket).
   - 🛠️ **Proposed Fix**: The corrected JSON code block.
   - ❓ **Permission Request**: Explicitly ask: *"Do you approve applying this fix to <file_name>? (Reply YES or NO)"*

### Step 4: Await Human Approval
1. Pause execution and wait for the user's response.
2. **If the user replies YES / APPROVE**:
   - Use your bash/exec tool to overwrite the target JSON file with the corrected raw JSON content.
   - Confirm successful repair to the user with a success message.
3. **If the user replies NO / CANCEL or requests changes**:
   - Abort the file update.
   - Ask the user how they would like to proceed.

## Output Format & Constraints
- Always maintain a professional, clear, and structured communication style in chat.
- Never bypass the bash execution or the human approval step under any circumstances.
