import ollama
import json

def get_llama_fix(broken_json_content):
    """
    Sends the broken JSON to the local Llama-3 model via Ollama
    to get a fixed version.
    """
    print("Requesting fix from Llama-3...")
    
    system_prompt = """
    You are an expert, automated JSON configuration repair agent.
    Your job is to fix syntax errors in JSON files (missing commas, brackets, etc.) and return ONLY the valid JSON content.
    
    STRICT RULES:
    1. Return ONLY the raw, corrected JSON code.
    2. Do NOT include any conversational text, explanations, or headers (e.g., no "Here is your fixed code").
    3. Do NOT use markdown formatting blocks (e.g., no ```json).
    4. Ensure the output is immediately parseable by a standard JSON library.
    """
    
    user_prompt = f"Broken JSON to fix:\n{broken_json_content}"

    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': user_prompt,
            },
        ])
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error communicating with Llama-3: {e}"

def main():
    file_path = "config.json"
    
    # Read the broken file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Try to parse it first (to confirm it's broken)
        try:
            json.loads(content)
            print("JSON is already valid.")
        except json.JSONDecodeError:
            print("JSON is broken as expected. Sending to Llama-3 for repair...")
            
            # Get fix from Llama-3
            fixed_content = get_llama_fix(content)
            
            print("\n--- Fixed JSON from Llama-3 ---")
            print(fixed_content)
            print("-------------------------------\n")
            
            # Verify if the fix is actually valid JSON
            try:
                json.loads(fixed_content)
                print("Llama-3 successfully fixed the JSON syntax!")
                
                # Optional: Overwrite the file with the fix
                # with open(file_path, 'w') as file:
                #     file.write(fixed_content)
                # print(f"File '{file_path}' has been updated with the fix.")
            except json.JSONDecodeError:
                print("Llama-3 provided a response, but it's still not valid JSON.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

if __name__ == "__main__":
    main()
