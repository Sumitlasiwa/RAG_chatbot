from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.services.ingestion_service import ingest_document
from schemas.chat import ChatRequest, ChatResponse
from schemas.ingestion import IngestionResponse
import os
import tempfile
from typing import Literal


router = APIRouter()

@router.post("/ingestions", response_model=IngestionResponse)
async def ingest(file: UploadFile = File(...),
                 chunker: Literal["CharacterTextSplitter", "RecursiveCharacterTextSplitter"] = Form("RecursiveCharacterTextSplitter")):
    allowed_types = {".pdf", ".txt"}
    suffix = os.path.splitext(file.filename)[1].lower()

    if suffix not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only .pdf and .txt files are supported.",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        result = ingest_document(temp_path, chunker=chunker)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)