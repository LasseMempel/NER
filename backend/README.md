# Secure NER Backend with GLiNER & Auth

NER API with JWT auth, async FastAPI, SQLite, and pre-loaded `knowledgator/gliner-x-large`.

## Features

- ✅ User registration & login (JWT)
- ✅ Async NER processing
- ✅ `gliner-x-large` model pre-downloaded in Docker
- ✅ Annotated texts saved per user
- ✅ Docker & conda support
- ✅ Swagger docs at `/docs`

## Setup

### 1. Clone

```bash
git clone https://github.com/your-org/NER.git
cd NER/backend