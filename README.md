# Face Attendance System

AI Face Recognition Attendance System built with:

- FastAPI
- PostgreSQL + pgvector
- InsightFace (ArcFace)
- Docker

## Features

- Employee Management
- Face Enrollment (multi-angle)
- Face Recognition (cosine similarity)
- Check-in / Check-out
- Attendance History

## Architecture

```
Camera / Upload Image
        │
        ▼
   InsightFace
   (Face Detection + Recognition)
        │
        ▼
   Embedding (512-d)
        │
        ▼
   pgvector Search (cosine distance)
        │
        ▼
   Matched Employee
        │
        ▼
   Attendance Service
        │
        ▼
   PostgreSQL
```

## Run Project

```bash
# Docker
docker compose up -d

# Install dependencies
uv sync

# Run server
uv run uvicorn app.main:app --reload
```

## API Docs

http://localhost:8000/docs

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL

**AI:**
- InsightFace (buffalo_l)
- ArcFace (recognition)
- RetinaFace (detection)

**Database:**
- pgvector (vector search)

**Deployment:**
- Docker
