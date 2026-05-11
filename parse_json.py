import json

def parse_broken_json(file_path):
    """
    Attempts to open and parse a JSON file.
    Designed to catch and report errors for broken JSON.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("Successfully parsed JSON:")
            print(data)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in '{file_path}'.")
        print(f"Details: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Pointing to the broken config.json created earlier
    parse_broken_json("config.json")
