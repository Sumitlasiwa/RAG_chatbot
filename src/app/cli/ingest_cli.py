from src.app.services.ingestion_service import ingest_document
from src.app.config import CHUNK_SIZE, CHUNK_OVERLAP, BATCH_SIZE

def main():
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
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                batch_size=BATCH_SIZE,
            )
            print(f"Ingestion completed: {result}")
        except Exception as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
