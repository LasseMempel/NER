# NER Backend with GLiNER

Minimal FastAPI backend for Named Entity Recognition using GLiNER and SQLite.

## Features
- User text input → NER via GLiNER
- Annotated text and entities saved in SQLite
- REST API with FastAPI
- Docker-ready deployment
- Anaconda environment management

## Setup

### Local Development (with conda)

```bash
git clone https://github.com/your-org/NER.git
cd backend

# Create conda environment
conda env create -f environment.yml
conda activate ner-backend

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000