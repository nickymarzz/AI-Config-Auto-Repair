import ollama

def test_llama():
    print("Testing Llama-3 connection...")
    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': 'What is 2+2?',
            },
        ])
        print("\nLlama-3 Response:")
        print(response['message']['content'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_llama()
