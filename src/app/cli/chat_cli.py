from src.app.services.chat_service import chat_pipeline

def main():
    user_id = input("User ID: ").strip()

    print("Type 'exit' to quit.")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Goodbye")
            break

        if not query:
            continue

        try:
            response = chat_pipeline(user_id=user_id, query=query)
            print(f"Bot: {response}")
        except Exception as exc:
            print(f"Error: {exc}")
        print("-"*50)

if __name__ == "__main__":
    main()
