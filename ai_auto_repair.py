import sys
import os
import re
import time
import json
import subprocess
import urllib.request
import urllib.error
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ── Configuration ──────────────────────────────────────────────────────────────
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "558503791")
TELEGRAM_BOT_TOKEN = "8725156361:AAG9MDvjIdbw84PI9fP9ew9MUuCkdFDPywY"
OPENCLAW_CLI = "/home/u_s_e_r/.npm-global/bin/openclaw"

# OpenRouter API (DeepSeek v4 Flash — Free Tier)
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "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"
)
OPENROUTER_MODEL = "openrouter/free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ── OpenRouter / DeepSeek Helper ───────────────────────────────────────────────
def extract_json_from_text(text):
    """Extract the first valid JSON object from text that may contain reasoning/markdown."""
    if not text:
        return None
    
    # Try the whole text first
    try:
        json.loads(text)
        return text
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Remove markdown fences and try again
    cleaned = re.sub(r'```(?:json)?\s*', '', text)
    cleaned = cleaned.strip()
    try:
        json.loads(cleaned)
        return cleaned
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Find JSON object pattern: first { to last }
    match = re.search(r'(\{[\s\S]*\})', text)
    if match:
        candidate = match.group(1)
        try:
            json.loads(candidate)
            return candidate
        except (json.JSONDecodeError, ValueError):
            pass
    
    return None


def call_deepseek(prompt):
    """Call DeepSeek v4 Flash via OpenRouter to generate a JSON repair."""
    payload = json.dumps({
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a JSON syntax repair assistant. When given broken JSON, return ONLY the corrected valid JSON. No explanation, no markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2048,
        "temperature": 0.1
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/ai-config-auto-repair",
            "X-Title": "AI Config Auto Repair"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            message = result["choices"][0]["message"]
            
            # DeepSeek reasoning models: content = final answer, reasoning_content = thinking
            content = message.get("content")
            reasoning = message.get("reasoning_content") or message.get("reasoning")
            
            print(f"[OPENROUTER] content={'present' if content else 'null'}, reasoning={'present' if reasoning else 'null'}")
            
            # Try content first (the actual answer), then reasoning as fallback
            for source_name, source_text in [("content", content), ("reasoning", reasoning)]:
                if source_text:
                    extracted = extract_json_from_text(source_text)
                    if extracted:
                        print(f"[OPENROUTER] ✅ Extracted valid JSON from '{source_name}' field")
                        return extracted
                    print(f"[OPENROUTER] '{source_name}' field has text but no valid JSON found")
            
            # Debug: show raw response
            print(f"[OPENROUTER DEBUG] Raw message keys: {list(message.keys())}")
            if content:
                print(f"[OPENROUTER DEBUG] content (first 300 chars): {content[:300]}")
            if reasoning:
                print(f"[OPENROUTER DEBUG] reasoning (first 300 chars): {reasoning[:300]}")
            return None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[OPENROUTER ERROR] HTTP {e.code}: {body[:500]}")
        return None
    except Exception as e:
        print(f"[OPENROUTER ERROR] {e}")
        return None

# ── Telegram Helpers ───────────────────────────────────────────────────────────
def send_telegram(message):
    """Send a message to Telegram via OpenClaw CLI."""
    try:
        result = subprocess.run(
            ["wsl", OPENCLAW_CLI, "message", "send",
             "--channel", "telegram",
             "--target", TELEGRAM_CHAT_ID,
             "--message", message],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False


def get_latest_telegram_message():
    """Read the latest Telegram message from OpenClaw's local session log via WSL."""
    try:
        log_path = "/home/u_s_e_r/.openclaw/agents/main/sessions/sessions.json.telegram-messages.json"
        result = subprocess.run(
            ["wsl", "tail", "-n", "10", log_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout:
            lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
            parsed_messages = []
            for line in lines:
                try:
                    data = json.loads(line)
                    msg = data.get("node", {}).get("sourceMessage", {})
                    chat_id = str(msg.get("chat", {}).get("id", ""))
                    text = (msg.get("text") or "").strip().upper()
                    date = msg.get("date", 0)
                    if chat_id == TELEGRAM_CHAT_ID:
                        parsed_messages.append({"text": text, "date": date})
                except Exception:
                    pass
            if parsed_messages:
                parsed_messages.sort(key=lambda x: x["date"])
                return parsed_messages[-1]
    except Exception as e:
        print(f"[TELEGRAM READ ERROR] {e}")
    return None


def poll_telegram_reply(timeout_seconds=300, poll_interval=3):
    """Poll OpenClaw's Telegram message log for a YES/NO reply from the user."""
    print(f"[POLL] Waiting up to {timeout_seconds}s for Telegram reply (YES/NO)...")
    
    # Get baseline date so we only react to NEW messages sent AFTER we asked
    initial_msg = get_latest_telegram_message()
    baseline_date = initial_msg["date"] if initial_msg else (time.time() - 10)
    
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        latest = get_latest_telegram_message()
        if latest and latest["date"] > baseline_date:
            text = latest["text"]
            if text in ("YES", "Y", "APPROVE"):
                return "YES"
            elif text in ("NO", "N", "REJECT", "CANCEL"):
                return "NO"
            else:
                baseline_date = latest["date"]
                print(f"[POLL] Got '{text}' — expected YES or NO")
                send_telegram("⚠️ Please reply with YES to approve or NO to reject.")
        
        time.sleep(poll_interval)
    
    return None  # Timeout

# ── Core Repair Logic ──────────────────────────────────────────────────────────
class AutoRepairHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file
        self.pending_fix = None
        self.awaiting_reply = False
        self._debounce_ts = 0

    def on_modified(self, event):
        now = time.time()
        if now - self._debounce_ts < 2:
            return
        self._debounce_ts = now

        if event.src_path.endswith(os.path.basename(self.target_file)):
            if self.awaiting_reply:
                return
            print(f"\n--- Change detected in {self.target_file} ---")
            self.process_file()

    def process_file(self):
        try:
            with open(self.target_file, 'r') as file:
                content = file.read()

            if not content.strip():
                return

            try:
                json.loads(content)
                print("[OK] JSON is valid. ✅")
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON is broken: {e}")
                self.handle_broken_json(content, e)

        except Exception as e:
            print(f"Error during processing: {e}")

    def handle_broken_json(self, broken_content, error):
        """Full repair workflow: DeepSeek Flash → Telegram → YES/NO → Apply."""
        if not TELEGRAM_CHAT_ID:
            print("[NOTE] TELEGRAM_CHAT_ID not set.")
            return

        # ── Step 1: Ask DeepSeek Flash for a fix ──────────────────────
        print(f"[STEP 1] Asking DeepSeek v4 Flash ({OPENROUTER_MODEL}) to generate a fix...")

        prompt = (
            f"The following JSON file has a syntax error:\n"
            f"Error: {error}\n\n"
            f"Broken JSON content:\n{broken_content}\n\n"
            f"Fix ALL syntax errors and return ONLY the corrected valid JSON."
        )

        fixed_json = call_deepseek(prompt)

        if not fixed_json:
            print("[ERROR] DeepSeek failed to generate a fix.")
            send_telegram(
                f"🚨 Watchdog Alert: JSON syntax error in config.json:\n{error}\n\n"
                f"⚠️ DeepSeek could not generate a fix. Please repair manually."
            )
            return

        # Pretty-print the validated JSON (call_deepseek already validated it)
        try:
            parsed = json.loads(fixed_json)
            fixed_json = json.dumps(parsed, indent=2)
            print("[STEP 1] ✅ DeepSeek generated valid JSON fix.")
        except json.JSONDecodeError as ve:
            print(f"[ERROR] DeepSeek's fix is not valid JSON: {ve}")
            send_telegram(
                f"🚨 Watchdog Alert: JSON syntax error in config.json:\n{error}\n\n"
                f"⚠️ AI generated an invalid fix. Please repair manually."
            )
            return

        self.pending_fix = fixed_json

        # ── Step 2: Send proposed fix to Telegram ─────────────────────
        print("[STEP 2] Sending proposed fix to Telegram...")

        telegram_msg = (
            f"🚨 Watchdog Alert\n"
            f"Syntax error in config.json:\n{error}\n\n"
            f"🛠️ Proposed Fix (by {OPENROUTER_MODEL}):\n{fixed_json}\n\n"
            f"Do you approve applying this fix?\n"
            f"👉 Reply YES to apply or NO to reject."
        )

        if send_telegram(telegram_msg):
            print("[STEP 2] ✅ Proposed fix sent to Telegram!")
        else:
            print("[ERROR] Failed to send to Telegram.")
            return

        # ── Step 3: Poll Telegram for YES/NO reply ────────────────────
        print("\n" + "=" * 60)
        print("📱 Waiting for your reply on Telegram (YES / NO)...")
        print("=" * 60)

        self.awaiting_reply = True
        try:
            reply = poll_telegram_reply(timeout_seconds=300)

            if reply == "YES":
                self.apply_fix()
            elif reply == "NO":
                print("[REJECTED] Fix was rejected via Telegram.")
                send_telegram("❌ Fix was rejected. No changes made to config.json.")
                self.pending_fix = None
            else:
                print("[TIMEOUT] No reply received within 5 minutes.")
                send_telegram("⏰ Approval timed out. No changes made to config.json.")
                self.pending_fix = None
        except KeyboardInterrupt:
            print("\n[CANCELLED] Approval cancelled.")
            self.pending_fix = None
        finally:
            self.awaiting_reply = False

    def apply_fix(self):
        """Write the approved fix to the target file."""
        if not self.pending_fix:
            print("[ERROR] No pending fix to apply.")
            return

        try:
            with open(self.target_file, 'w') as f:
                f.write(self.pending_fix)
            print(f"[SUCCESS] ✅ Fix applied to {self.target_file}!")
            send_telegram("✅ Fix has been applied to config.json! File is now valid.")

            # Verify
            with open(self.target_file, 'r') as f:
                json.loads(f.read())
            print("[VERIFY] ✅ File is valid JSON after repair.")

        except Exception as e:
            print(f"[ERROR] Failed to apply fix: {e}")
            send_telegram(f"❌ Error applying fix: {e}")
        finally:
            self.pending_fix = None


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(script_dir, "config.json")

    event_handler = AutoRepairHandler(target)
    observer = Observer()
    observer.schedule(event_handler, script_dir, recursive=False)

    print("=" * 60)
    print("  🤖 AI Auto-Repair System (Human-in-the-loop)")
    print(f"  🧠 Model: {OPENROUTER_MODEL}")
    print(f"  📱 Telegram Chat: {TELEGRAM_CHAT_ID}")
    print("=" * 60)
    print(f"Watching '{target}' for errors...\n")

    # Run an initial check
    event_handler.process_file()

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping watchdog...")
        observer.stop()
    observer.join()
