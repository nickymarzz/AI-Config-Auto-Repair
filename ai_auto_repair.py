import sys
import time
import json
import ollama
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutoRepairHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file
        self.system_prompt = """
        You are an expert, automated JSON configuration repair agent.
        Your job is to fix syntax errors in JSON files (missing commas, brackets, etc.) and return ONLY the valid JSON content.
        
        STRICT RULES:
        1. Return ONLY the raw, corrected JSON code.
        2. Do NOT include any conversational text, explanations, or headers.
        3. Do NOT use markdown formatting blocks (e.g., no ```json).
        4. Ensure the output is immediately parseable by a standard JSON library.
        """

    def on_modified(self, event):
        if event.src_path.endswith(self.target_file):
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
                print("[OK] JSON is valid.")
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON is broken: {e}")
                
                max_retries = 3
                attempt = 0
                fixed_content = None
                
                while attempt < max_retries:
                    attempt += 1
                    print(f"[AI] Requesting repair from Llama-3 (Attempt {attempt}/{max_retries})...")
                    
                    # Pass the error message to help the AI focus
                    fixed_content = self.repair_with_llama(content, str(e))
                    
                    if fixed_content:
                        try:
                            # Advanced Error Handling: Validate the LLM output
                            json.loads(fixed_content)
                            print("\n--- Proposed Fix ---")
                            print(fixed_content)
                            print("--------------------\n")
                            
                            # Human-in-the-loop: Wait for explicit approval
                            choice = input("Do you want to apply this fix? (Y/n): ").strip().lower()
                            if choice == 'y' or choice == '':
                                with open(self.target_file, 'w') as file:
                                    file.write(fixed_content)
                                print("[SUCCESS] File repaired and updated!")
                                return
                            else:
                                print("[ACTION] Repair cancelled by user.")
                                return
                        except json.JSONDecodeError:
                            print(f"[AI ERROR] Llama-3 output was not valid JSON. Retrying...")
                            # The loop will try again
                    else:
                        print("[ERROR] Failed to get response from Llama-3.")
                        break
                
                if attempt == max_retries:
                    print("[FATAL] Could not repair JSON after multiple attempts.")

        except Exception as e:
            print(f"Error during processing: {e}")

    def repair_with_llama(self, broken_content, error_msg):
        user_prompt = f"Broken JSON:\n{broken_content}\n\nError Message:\n{error_msg}"
        try:
            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None

if __name__ == "__main__":
    path = "."
    target = "config.json"
    
    event_handler = AutoRepairHandler(target)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print("AI Auto-Repair System (Human-in-the-loop) Active.")
    print(f"Watching '{target}' for errors...")
    
    # We use -u flag for unbuffered output to ensure the input prompt is visible
    # Run an initial check
    event_handler.process_file()
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
