# Attendance Flow

## Employee Register Face

```
Upload Images (multi-angle: front, left, right, up, down)
    │
    ▼
Validate Angles (allowed: front, left, right, up, down)
    │
    ▼
Check Duplicate Angles (same request)
    │
    ▼
Check Existing Active Embeddings (DB)
    │
    ▼
Extract Embeddings (InsightFace - buffalo_l)
    │
    ▼
Save Images to /uploads/faces/{employee_code}/
    │
    ▼
Store Embeddings in PostgreSQL (vector(512))
    │
    ▼
Face Enrollment Complete
```

### Validation Rules

1. **Number of files = Number of angles** - Each file must have a corresponding angle
2. **Allowed angles** - Only: `front`, `left`, `right`, `up`, `down`
3. **No duplicate angles** - Cannot register same angle twice in one request
4. **No duplicate active embeddings** - If employee already has active embedding for an angle, reject

---

## Check-in Flow

```
Upload Image
    │
    ▼
Extract Embedding (InsightFace)
    │
    ▼
Cosine Distance Search (pgvector)
    │
    ▼
Distance ≤ 0.55?
    │
    ├── NO → "Face not recognized"
    │
   YES
    │
    ▼
Already checked in today?
    │
    ├── YES → "Already checked in today"
    │
    NO
    │
    ▼
INSERT attendance_log
    │
    ▼
Return Success
```

### Response

**Success:**
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

**Already checked in:**
```json
{
  "success": false,
  "message": "Already checked in today"
}
```

---

## Check-out Flow

```
Upload Image
    │
    ▼
Extract Embedding (InsightFace)
    │
    ▼
Cosine Distance Search (pgvector)
    │
    ▼
Distance ≤ 0.55?
    │
    ├── NO → "Face not recognized"
    │
   YES
    │
    ▼
Has check-in today?
    │
    ├── NO → "No check-in found for today"
    │
   YES
    │
    ▼
Already checked out?
    │
    ├── YES → "Already checked out today"
    │
    NO
    │
    ▼
UPDATE check_out_time
    │
    ▼
Return Success
```

### Response

**Success:**
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

**No check-in:**
```json
{
  "success": false,
  "message": "No check-in found for today"
}
```

---

## Recognition Logic

### Cosine Distance

- `0` = Identical face
- `0.0 - 0.4` = Very similar
- `0.4 - 0.55` = Similar (match)
- `0.55 - 0.8` = Different (no match)
- `> 0.8` = Completely different

### Threshold

Default: `0.55` (configured in `app/core/config.py`)

```python
FACE_RECOGNITION_THRESHOLD = 0.55
```

### Embedding Model

- Model: InsightFace buffalo_l
- Dimensions: 512
- Detection: RetinaFace
- Recognition: ArcFace

---

## Business Rules

1. **1 employee = 1 check-in per day** - Duplicate check-in rejected
2. **Check-out requires check-in** - Must check-in before check-out
3. **1 check-out per day** - Cannot check-out twice
4. **UTC timestamps** - All times stored in UTC
5. **Confidence score** - Face detection confidence from RetinaFace
6. **Recognition distance** - Cosine distance for audit/debug
