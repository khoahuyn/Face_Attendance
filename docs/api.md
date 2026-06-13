# API Reference

Base URL: `http://localhost:8000`

---

## Employees

### List Employees

```
GET /employees/
```

**Response:**
```json
[
  {
    "id": 1,
    "employee_code": "NV001",
    "full_name": "Nguyen Van A",
    "department": "IT",
    "position": "Developer",
    "status": "active"
  }
]
```

### Get Employee

```
GET /employees/{employee_id}
```

### Create Employee

```
POST /employees/
```

**Request:**
```json
{
  "employee_code": "NV001",
  "full_name": "Nguyen Van A",
  "department": "IT",
  "position": "Developer"
}
```

### Register Face

```
POST /employees/{employee_id}/register-face
```

**Request:** `multipart/form-data`
- `files`: Face images (multi-angle)
- `angles`: Comma-separated angles (e.g., `front,left,right,up,down`)

**Allowed angles:** `front`, `left`, `right`, `up`, `down`

---

## Face Embeddings

### List Embeddings

```
GET /face-embeddings/
```

**Query Params:**
- `employee_id` (optional)

### List Active Embeddings

```
GET /face-embeddings/active
```

### Create Embedding

```
POST /face-embeddings/
```

**Request:**
```json
{
  "employee_id": 1,
  "embedding": [0.1, 0.2, ...],
  "angle": "front",
  "confidence": 0.95
}
```

### Recognize Face (by embedding)

```
POST /face-embeddings/recognize
```

**Request:**
```json
{
  "embedding": [0.1, 0.2, ...]
}
```

**Query Params:**
- `limit`: Max results (default: 5)

### Recognize Face (by image)

```
POST /face-embeddings/recognize-image
```

**Request:** `multipart/form-data`
- `file`: Face image

**Response:**
```json
{
  "employee_id": 1,
  "employee_code": "NV001",
  "full_name": "Nguyen Van A",
  "distance": 0.34,
  "matched": true
}
```

### Deactivate Embedding

```
PATCH /face-embeddings/{embedding_id}/deactivate
```

---

## Attendance

### Check-in

```
POST /attendance/checkin
```

**Request:** `multipart/form-data`
- `file`: Face image
- `camera_id` (optional): Camera identifier

**Response:**
```json
{
  "success": true,
  "employee_id": 1,
  "employee_code": "NV001",
  "full_name": "Nguyen Van A",
  "check_in_time": "2026-06-13T01:00:00+00:00",
  "confidence": 0.92,
  "distance": 0.34
}
```

**Error Responses:**
```json
{
  "success": false,
  "message": "Face not recognized"
}
```

```json
{
  "success": false,
  "message": "Already checked in today"
}
```

### Check-out

```
POST /attendance/checkout
```

**Request:** `multipart/form-data`
- `file`: Face image

**Response:**
```json
{
  "success": true,
  "employee_id": 1,
  "employee_code": "NV001",
  "full_name": "Nguyen Van A",
  "check_in_time": "2026-06-13T01:00:00+00:00",
  "check_out_time": "2026-06-13T10:00:00+00:00",
  "confidence": 0.91,
  "distance": 0.36
}
```

**Error Responses:**
```json
{
  "success": false,
  "message": "No check-in found for today"
}
```

```json
{
  "success": false,
  "message": "Already checked out today"
}
```

### Get Attendance Logs

```
GET /attendance/
```

**Query Params:**
- `employee_id` (optional)
- `from` (optional): Start date (YYYY-MM-DD)
- `to` (optional): End date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "employee_id": 1,
    "work_date": "2026-06-13",
    "check_in_time": "2026-06-13T01:00:00+00:00",
    "check_out_time": "2026-06-13T10:00:00+00:00",
    "camera_id": null,
    "confidence_score": 0.92,
    "recognition_distance": 0.34,
    "created_at": "2026-06-13T01:00:00+00:00"
  }
]
```

---

## Swagger UI

Interactive API docs available at:

```
http://localhost:8000/docs
```
