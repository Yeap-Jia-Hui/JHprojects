import ollama
import sys

def main():
    print("=== Ollama Chat ===")
    print("Type 'quit' to exit\n")
    sys.stdout.flush()
    
    while True:
        try:
            user_input = input("Enter message: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            if not user_input:
                continue
            
            print(f"\nYou: {user_input}")
            sys.stdout.flush()
            
            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            
            assistant_response = response["message"]["content"]
            print(f"Assistant: {assistant_response}\n")
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()