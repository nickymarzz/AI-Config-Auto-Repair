import sys
import json
import os

def validate(file_path):
    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": f"File not found: {file_path}"}))
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if not content.strip():
            print(json.dumps({"status": "valid", "message": "File is empty."}))
            return

        json.loads(content)
        print(json.dumps({"status": "valid", "message": "JSON is valid."}))
    except json.JSONDecodeError as e:
        error_details = {
            "status": "error",
            "message": str(e),
            "line": e.lineno,
            "column": e.colno,
            "error": e.msg
        }
        print(json.dumps(error_details))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No file path provided."}))
        sys.exit(1)
    validate(sys.argv[1])
