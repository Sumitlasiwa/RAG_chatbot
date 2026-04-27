from uuid import uuid4

from app.services.chat_service import chat_pipeline


def create_session_id():
    return uuid4().hex

def main():
    session_id = create_session_id()

    print(f"Session started: {session_id}")
    print("Type 'exit' to quit.")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Goodbye")
            break

        if not query:
            continue

        try:
            response = chat_pipeline(user_id=session_id, query=query)
            print(f"Bot: {response}")
        except Exception as exc:
            print(f"Error: {exc}")
        print("-"*50)

if __name__ == "__main__":
    main()
