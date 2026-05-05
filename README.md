# Personal Chatbot

Portfolio-focused RAG chatbot for answering questions about Sumit's work, skills, and projects.

## Overview

This project is a document-based chatbot built with FastAPI, LangChain, Pinecone, MongoDB, Redis, and Hugging Face.

It ingests `.pdf` and `.txt` files, stores chunk embeddings in Pinecone, keeps document metadata in MongoDB, and saves short chat history in Redis.

## Features

- Portfolio-specific chatbot with strict knowledge-base scoping
- Document ingestion for `.pdf` and `.txt` files
- Retrieval-augmented generation (RAG) pipeline
- FastAPI endpoint for chat requests
- CLI tools for ingestion and local chat testing
- Redis-based short-term conversation memory

## Tech Stack

- Python
- FastAPI
- LangChain
- Pinecone
- MongoDB
- Redis
- Hugging Face

## Project Structure

```text
src/
|-- api/                 # FastAPI app
|-- app/
|   |-- cli/             # CLI tools
|   |-- db/              # MongoDB, Redis, Pinecone integrations
|   |-- services/        # Chat, RAG, ingestion services
|   `-- utils/           # File loading, chunking, prompts
`-- schemas/             # Request/response schemas
tests/                   # Test files
KB/                      # Knowledge base files
```

## Requirements

Make sure these are available before running the project:

- Python 3.11+
- MongoDB
- Redis
- Pinecone account and API key
- A Pinecone index created in advance
- Hugging Face access token for the configured LLM

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sumitlasiwa/RAG_chatbot
cd Chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=your_mongodb_connection_string
PINECONE_TOKEN=your_pinecone_api_key
REDIS_URL=redis://localhost:6379/0
PINECONE_INDEX_NAME=documentstore
EMBEDDING_MODEL_NAME=llama-text-embed-v2
EMBEDDING_DIMENSION=384
LLM_REPO_ID=Qwen/Qwen2.5-7B-Instruct
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
CHUNK_SIZE=400
CHUNK_OVERLAP=50
BATCH_SIZE=50
```

Notes:

- `HUGGINGFACEHUB_ACCESS_TOKEN` and `HF_TOKEN` are also accepted for the Hugging Face token.
- The Pinecone index must already exist and its dimension must match `EMBEDDING_DIMENSION`.

## Running the Project

### Start the API server

```bash
$env:PYTHONPATH="src"
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Run the chat CLI

```bash
$env:PYTHONPATH="src"
python -m app.cli.chat_cli
```

### Run the ingestion CLI

```bash
$env:PYTHONPATH="src"
python -m app.cli.ingest_cli
```

When prompted, enter the path to a `.pdf` or `.txt` file to ingest.

## API

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "chatbot-api"
}
```

### Root endpoint

```http
GET /
```

Example response:

```json
{
  "message": "Personal chatbot"
}
```

### Chat endpoint

```http
POST /chats
```

Example request body:

```json
{
  "user_id": "demo-user",
  "query": "Tell me about Sumit's projects"
}
```

## Testing

Run tests with:

```bash
$env:PYTHONPATH="src"
pytest
```

Note:

- The test suite expects `pytest` to be installed in your environment.

## Notes

- The chatbot is designed to answer only from Sumit's portfolio knowledge base.
- Unsupported questions are intentionally refused.
- Supported ingestion formats are `.pdf` and `.txt`.
- The project uses Pinecone hosted embeddings for retrieval.
