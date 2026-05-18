from pydantic import BaseModel

class IngestionResponse(BaseModel):
    file_name: str
    chunks_inserted: int