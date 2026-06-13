# Database Schema

## Tables

### employees

| Field | Type | Constraint |
|-------|------|------------|
| id | SERIAL | PRIMARY KEY |
| employee_code | VARCHAR(50) | UNIQUE, NOT NULL |
| full_name | VARCHAR(255) | NOT NULL |
| department | VARCHAR(255) | NULLABLE |
| position | VARCHAR(255) | NULLABLE |
| status | VARCHAR(50) | DEFAULT 'active' |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    position VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### face_embeddings

| Field | Type | Constraint |
|-------|------|------------|
| id | SERIAL | PRIMARY KEY |
| employee_id | INTEGER | FK → employees.id, ON DELETE CASCADE |
| embedding | VECTOR(512) | NOT NULL |
| angle | VARCHAR(20) | NOT NULL |
| face_image_path | VARCHAR(500) | NULLABLE |
| confidence | FLOAT | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| device_name | VARCHAR(255) | NULLABLE |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |

```sql
CREATE TABLE face_embeddings (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    embedding VECTOR(512) NOT NULL,
    angle VARCHAR(20) NOT NULL,
    face_image_path VARCHAR(500),
    confidence FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    device_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### attendance_logs

| Field | Type | Constraint |
|-------|------|------------|
| id | SERIAL | PRIMARY KEY |
| employee_id | INTEGER | FK → employees.id, ON DELETE CASCADE |
| work_date | DATE | NOT NULL |
| check_in_time | TIMESTAMPTZ | NULLABLE |
| check_out_time | TIMESTAMPTZ | NULLABLE |
| camera_id | VARCHAR(255) | NULLABLE |
| confidence_score | FLOAT | NOT NULL |
| recognition_distance | FLOAT | NOT NULL |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |

**Unique Constraint:** `(employee_id, work_date)`

```sql
CREATE TABLE attendance_logs (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    work_date DATE NOT NULL,
    check_in_time TIMESTAMPTZ,
    check_out_time TIMESTAMPTZ,
    camera_id VARCHAR(255),
    confidence_score FLOAT NOT NULL,
    recognition_distance FLOAT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(employee_id, work_date)
);
```

---

## Relationships

```
Employee
    │
    ├──< FaceEmbedding (1:N)
    │       employee_id → employees.id
    │
    └──< AttendanceLog (1:N)
            employee_id → employees.id
```

---

## Indexes

```sql
-- Face embedding search (pgvector)
CREATE INDEX ON face_embeddings
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Attendance lookup
CREATE INDEX ON attendance_logs (employee_id, work_date);
```

---

## Notes

- **VECTOR(512)**: 512-dimensional face embedding from InsightFace
- **Cosine distance**: Used for face matching (`<=>` operator)
- **is_active**: Soft delete for face embeddings
- **work_date**: One record per employee per day (UNIQUE constraint)
- **recognition_distance**: Cosine distance at recognition time (for audit)
