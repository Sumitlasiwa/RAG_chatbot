from app.services.ingestion_service import ingest_document
from app.config import get_settings

def main():
    settings = get_settings()
    print("Type a file path to ingest, or 'exit' to quit.")

    while True:
        file_path = input("File path: ").strip()

        if file_path.lower() == "exit":
            print("Goodbye")
            break

        if not file_path:
            continue

        try:
            result = ingest_document(
                file_path=file_path,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                batch_size=settings.batch_size,
            )
            print(f"Ingestion completed: {result}")
        except Exception as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
