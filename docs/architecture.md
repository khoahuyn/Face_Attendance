# System Architecture

## Overview

```
┌──────────────┐
│   Frontend   │
│  (Web/Mobile)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FastAPI    │
│   Backend    │
└──────┬───────┘
       │
 ┌─────┴─────┐
 │           │
 ▼           ▼
┌────────┐ ┌────────────┐
│Postgres│ │InsightFace │
│pgvector│ │  ArcFace   │
└────────┘ └────────────┘
```

## Components

### FastAPI Backend
- REST API endpoints
- Request validation (Pydantic)
- Dependency injection (DB session)

### PostgreSQL + pgvector
- Employee data storage
- Face embedding storage (vector(512))
- Cosine distance search
- Attendance log storage

### InsightFace (AI)
- Face detection (RetinaFace)
- Face recognition (ArcFace)
- 512-dimensional embeddings
- Model: buffalo_l

## Project Structure

```
app/
├── main.py                    # FastAPI app
├── core/
│   ├── config.py              # Settings
│   ├── database.py            # DB engine
│   └── dependencies.py        # get_db()
├── models/
│   ├── base.py                # SQLAlchemy Base
│   ├── employee.py            # Employee model
│   ├── face_embedding.py      # FaceEmbedding model
│   └── attendance.py          # AttendanceLog model
├── schemas/
│   ├── employee.py            # Employee schemas
│   ├── face_embedding.py      # Face schemas
│   ├── face_registration.py   # Registration schemas
│   └── attendance.py          # Attendance schemas
├── routers/
│   ├── employee.py            # /employees/*
│   ├── face_embedding.py      # /face-embeddings/*
│   └── attendance.py          # /attendance/*
├── services/
│   ├── employee.py            # EmployeeService
│   ├── face_embedding.py      # FaceEmbeddingService
│   └── attendance.py          # AttendanceService
└── ai/
    └── face_recognition_service.py  # InsightFace wrapper
```

## Data Flow

```
Employee Register Face
    │
    ▼
Upload Images (multi-angle)
    │
    ▼
Extract Embeddings (InsightFace)
    │
    ▼
Store in PostgreSQL (pgvector)
    │
    ▼
Face Embeddings Ready

---

Check-in / Check-out
    │
    ▼
Upload Image
    │
    ▼
Extract Embedding
    │
    ▼
Cosine Distance Search (pgvector)
    │
    ▼
Match Employee (threshold ≤ 0.55)
    │
    ▼
Create/Update Attendance Log
```
