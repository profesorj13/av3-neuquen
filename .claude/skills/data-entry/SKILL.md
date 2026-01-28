---
name: data-entry
description: Expert data entry for the educational planning database. Use this skill to add, modify, or query users, areas, subjects, courses, schedules, coordination documents, and all other database entities.
---

# Data Entry Expert - Educational Planning System

You are an expert data entry operator for this educational planning system. When the user asks to add, modify, or query data, execute the appropriate SQL commands.

## Database Connection

```bash
psql "postgresql://postgres:postgres@localhost:5480/av3"
```

---

## Complete Database Schema

### 1. users
Teachers and coordinators.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:**
| ID | Name |
|----|------|
| 1 | Coordinador Demo 1 |
| 2 | Coordinador Demo 2 |

### 2. areas
Subject groupings with a coordinator.

```sql
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    coordinator_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data (7 areas):**
| ID | Name | Coordinator |
|----|------|-------------|
| 1 | Cs. Sociales, Políticas y Económicas | Coordinador Demo 1 (ID 1) |
| 2 | Lenguajes y Producción Cultural | Coordinador Demo 1 (ID 1) |
| 3 | Ciencias Naturales | Coordinador Demo 2 (ID 2) |
| 4 | Matemática - Informática | Coordinador Demo 2 (ID 2) |
| 5 | Integración Tecnológica | Coordinador Demo 1 (ID 1) |
| 6 | EFI | Coordinador Demo 2 (ID 2) |
| 7 | ESI | Coordinador Demo 2 (ID 2) |

### 3. subjects
Individual subjects belonging to an area.

```sql
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    area_id INTEGER NOT NULL REFERENCES areas(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,  -- Contains disciplinary nucleus for Area 1 subjects
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data (18 subjects):**

**Area 1 - Cs. Sociales, Políticas y Económicas (5 subjects with disciplinary nuclei):**
| ID | Name | Disciplinary Nucleus (summary) |
|----|------|--------------------------------|
| 1 | Historia | Categorías de tiempo/territorio, sociedades igualitarias, división de trabajos, patriarcado, herida colonial |
| 2 | Geografía | Miradas pluriversales, bienes comunes, hegemonía europea, relaciones capitalistas heteropatriarcales |
| 3 | Economía | Poder-saber en satisfactores, economías del Buen Vivir, ecofeminismo, economía ecológica |
| 4 | Construcción de Ciudadanías | Binarismo humano/subhumano, deconstrucción de prácticas racistas, cuerpo-territorio |
| 5 | Filosofía | Ética en ordenamientos sociales, filosofías otras (tojolabal, Qom, Maya), principio de relacionalidad |

**Area 2 - Lenguajes y Producción Cultural (7 subjects):**
| ID | Name |
|----|------|
| 6 | Lengua |
| 7 | Literatura |
| 8 | Lenguas Otras (Inglés) |
| 9 | Artes Visuales |
| 10 | Comunicación y Medios |
| 11 | Lengua preexistente |
| 12 | Lengua y literatura |

**Area 3 - Ciencias Naturales (3 subjects):**
| ID | Name |
|----|------|
| 13 | Biología |
| 14 | Química |
| 15 | Física |

**Area 4 - Matemática-Informática (2 subjects):**
| ID | Name |
|----|------|
| 16 | Matemática |
| 17 | Informática |

**Area 5 - Integración Tecnológica (1 subject):**
| ID | Name |
|----|------|
| 18 | Integración tecnológica |

### 4. courses
Student groups (e.g., "2do año 1era") with weekly schedule.

```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    schedule JSONB,  -- Weekly schedule with time slots
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Schedule JSONB format:**
```json
{
  "monday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "07:45-08:25", "subject": "Informática"}
  ],
  "tuesday": [...],
  "wednesday": [...],
  "thursday": [...],
  "friday": [...]
}
```

**EPAs (shared classes)**: When two subjects share the same time slot, they appear as separate entries with identical `time` values.

**Current courses:**
| ID | Name |
|----|------|
| 1 | 2do año 1era |

**EPAs in "2do año 1era":**
- Lunes M1-M2: Matemática + Informática
- Lunes M3-M4: Economía + Geografía
- Lunes M5-M6: Historia + Construcción de Ciudadanías
- Miércoles M6-M7: Biología + Química
- Jueves M5-M6: Historia + Construcción de Ciudadanías
- Viernes M3-M4: Lengua y literatura + Lenguas Otras (Inglés)

### 5. students
Students enrolled in a course.

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:** None (no students seeded yet)

### 6. course_subjects
Assignment of a teacher to teach a subject in a course.

```sql
CREATE TABLE course_subjects (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    teacher_id INTEGER NOT NULL REFERENCES users(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    school_year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:** None (no teacher assignments seeded yet)

### 7. problematic_nuclei
High-level knowledge themes.

```sql
CREATE TABLE problematic_nuclei (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:**
| ID | Name | Description |
|----|------|-------------|
| 1 | Las lógicas de poder y saber | Las lógicas de poder y saber en las sociedades disputan en los territorios, el control sobre los bienes comunes, las sexualidades y sus productos, los trabajos y sus productos, y la subjetividad social, produciendo relaciones de dominación y explotación como génesis de la crisis civilizatoria. |

### 8. knowledge_areas
Specific knowledge domains under nuclei.

```sql
CREATE TABLE knowledge_areas (
    id SERIAL PRIMARY KEY,
    nucleus_id INTEGER NOT NULL REFERENCES problematic_nuclei(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:**
| ID | Nucleus | Name |
|----|---------|------|
| 1 | Las lógicas de poder y saber (1) | Revolución Neolítica |

### 9. categories
Granular skills/concepts to teach.

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    knowledge_area_id INTEGER NOT NULL REFERENCES knowledge_areas(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data (12 categories):**
| ID | Knowledge Area | Name |
|----|----------------|------|
| 1 | Revolución Neolítica (1) | Tiempos/territorios |
| 2 | Revolución Neolítica (1) | Subjetividad |
| 3 | Revolución Neolítica (1) | Trabajos |
| 4 | Revolución Neolítica (1) | Revolución |
| 5 | Revolución Neolítica (1) | Estado |
| 6 | Revolución Neolítica (1) | Acumulación |
| 7 | Revolución Neolítica (1) | Naturaleza |
| 8 | Revolución Neolítica (1) | Derechos |
| 9 | Revolución Neolítica (1) | Ética |
| 10 | Revolución Neolítica (1) | Necesidades |
| 11 | Revolución Neolítica (1) | Satisfactores |
| 12 | Revolución Neolítica (1) | Bienes Comunes |

### 10. coordination_documents
Planning documents created by coordinators.

```sql
CREATE TABLE coordination_documents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    area_id INTEGER NOT NULL REFERENCES areas(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',  -- draft, published, archived
    methodological_strategies TEXT,
    subjects_data JSONB,  -- Per-subject planning
    nucleus_ids INTEGER[] DEFAULT '{}',
    category_ids INTEGER[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**subjects_data JSONB format:**
```json
{
  "1": {  // subject_id as key
    "class_count": 5,
    "category_ids": [5, 6, 7],
    "class_plan": [
      {"class_number": 1, "title": "Introduction", "objective": "...", "category_ids": [5]},
      {"class_number": 2, "title": "Deep dive", "objective": "...", "category_ids": [5, 6]}
    ]
  },
  "2": {...}
}
```

**Current data:** None (no coordination documents seeded)

### 11. moment_types
Types of class moments (apertura, desarrollo, cierre).

```sql
CREATE TABLE moment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:**
| ID | Name |
|----|------|
| 1 | Apertura/Motivación |
| 2 | Desarrollo/Construcción/Práctica |
| 3 | Cierre/Metacognición |

### 12. activities
Didactic activities available for lesson planning.

```sql
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    moment_type VARCHAR(50),  -- apertura, desarrollo, cierre
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Current data:**
- Apertura (IDs 1-5): 5 activities for class opening
- Desarrollo (IDs 6-12): 7 activities for main development
- Cierre (IDs 13-16): 4 activities for class closing

### 13. teacher_lesson_plans
Individual lesson plans created by teachers.

```sql
CREATE TABLE teacher_lesson_plans (
    id SERIAL PRIMARY KEY,
    course_subject_id INTEGER NOT NULL REFERENCES course_subjects(id),
    coordination_document_id INTEGER NOT NULL REFERENCES coordination_documents(id),
    class_number INTEGER NOT NULL,
    title VARCHAR(255),
    category_ids INTEGER[] DEFAULT '{}',
    objective TEXT,
    knowledge_content TEXT,
    didactic_strategies TEXT,
    class_format VARCHAR(100),
    moments JSONB,  -- {apertura: {...}, desarrollo: {...}, cierre: {...}}
    status VARCHAR(50) DEFAULT 'pending',  -- pending, planned, completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_subject_id, coordination_document_id, class_number)
);
```

### 14. proposals
Templates for pedagogical proposals (e.g., "Simulador Anatómico").

```sql
CREATE TABLE proposals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration_weeks INTEGER DEFAULT 8,
    tools JSONB DEFAULT '[]',
    curriculum_card JSONB DEFAULT '{}',
    alizia_info JSONB DEFAULT '{}',
    initial_agreements JSONB DEFAULT '[]',
    stages JSONB DEFAULT '[]',
    annexes JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    status VARCHAR(50) DEFAULT 'upcoming', -- 'completed', 'recommended', 'upcoming'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status values:**
- `completed`: Proposals that have been completed/finished ("Realizadas")
- `recommended`: The recommended/featured proposal ("Recomendada")
- `upcoming`: Future proposals not yet available ("Próximas")

### 15. proposal_progress
Tracks a teacher's progress through a proposal for a specific course_subject.

```sql
CREATE TABLE proposal_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    proposal_id INTEGER REFERENCES proposals(id) ON DELETE CASCADE,
    course_subject_id INTEGER REFERENCES course_subjects(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'not_started',
    agreements_data JSONB DEFAULT '{}',
    stages_data JSONB DEFAULT '{}',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, proposal_id, course_subject_id)
);
```

**Status values:** `not_started`, `in_progress`, `completed`

---

## Common Operations

### Add a new user (teacher or coordinator)
```sql
INSERT INTO users (email, name) VALUES ('email@test.com', 'Full Name');
```

### Add a new area
```sql
INSERT INTO areas (coordinator_id, name, description)
VALUES (1, 'Area Name', 'Description');
```

### Add a new subject to an area
```sql
INSERT INTO subjects (area_id, name, description)
VALUES (1, 'Subject Name', 'Disciplinary nucleus description');
```

### Add a new course with schedule
```sql
INSERT INTO courses (name, schedule) VALUES (
    '3er año 1era',
    '{"monday": [{"time": "07:45-08:25", "subject": "Matemática"}], "tuesday": [], "wednesday": [], "thursday": [], "friday": []}'
);
```

### Add a class slot to existing course schedule
```sql
UPDATE courses
SET schedule = jsonb_set(
    schedule,
    '{thursday}',
    (COALESCE(schedule->'thursday', '[]'::jsonb) || '[{"time": "10:40-11:20", "subject": "Biología"}]'::jsonb)
)
WHERE name = '2do año 1era';
```

### Add an EPA (shared class) - two subjects at same time
```sql
UPDATE courses
SET schedule = jsonb_set(
    schedule,
    '{friday}',
    (COALESCE(schedule->'friday', '[]'::jsonb) || '[{"time": "09:10-09:50", "subject": "Historia"}, {"time": "09:10-09:50", "subject": "Geografía"}]'::jsonb)
)
WHERE name = '2do año 1era';
```

### Add a student to a course
```sql
INSERT INTO students (course_id, name) VALUES (1, 'Student Name');
```

### Assign a teacher to a subject in a course
```sql
INSERT INTO course_subjects (course_id, subject_id, teacher_id, start_date, end_date, school_year)
VALUES (1, 1, 1, '2026-03-01', '2026-12-15', 2026);
```

### Create a coordination document
```sql
INSERT INTO coordination_documents (name, area_id, start_date, end_date, status, nucleus_ids, category_ids)
VALUES ('Document Name', 1, '2026-03-01', '2026-12-15', 'draft', '{1}', '{1,2,3,4,5}');
```

### Update document subjects_data
```sql
UPDATE coordination_documents
SET subjects_data = '{"1": {"class_count": 5, "category_ids": [1,2], "class_plan": []}}'::jsonb
WHERE id = 1;
```

### Publish a document
```sql
UPDATE coordination_documents SET status = 'published' WHERE id = 1;
```

### Add a problematic nucleus
```sql
INSERT INTO problematic_nuclei (name, description) VALUES ('Name', 'Description');
```

### Add a knowledge area
```sql
INSERT INTO knowledge_areas (nucleus_id, name, description) VALUES (1, 'Name', 'Description');
```

### Add a category
```sql
INSERT INTO categories (knowledge_area_id, name, description) VALUES (1, 'Name', 'Description');
```

### Create a proposal
```sql
INSERT INTO proposals (name, description, duration_weeks, tools, stages)
VALUES (
    'Proposal Name',
    'Description of the proposal',
    8,
    '["Scratch", "micro:bit"]',
    '[{"number": 1, "name": "Stage 1", "duration_classes": 2, "description": "...", "decisions": [], "resources": []}]'
);
```

### Start a proposal for a teacher (create progress)
```sql
INSERT INTO proposal_progress (user_id, proposal_id, course_subject_id, status, started_at)
VALUES (1, 1, 1, 'in_progress', NOW());
```

---

## Query Reference Data

### List all users
```sql
SELECT id, name, email FROM users ORDER BY id;
```

### List all areas with coordinators
```sql
SELECT a.id, a.name, u.name as coordinator FROM areas a JOIN users u ON a.coordinator_id = u.id;
```

### List all subjects with their areas
```sql
SELECT s.id, s.name, a.name as area FROM subjects s JOIN areas a ON s.area_id = a.id ORDER BY s.id;
```

### List subjects with disciplinary nuclei (Area 1)
```sql
SELECT s.id, s.name, LEFT(s.description, 80) as disciplinary_nucleus
FROM subjects s WHERE s.area_id = 1;
```

### List all courses with their schedules
```sql
SELECT id, name, schedule FROM courses;
```

### List EPAs (shared classes) for a course
```sql
-- Shows time slots that appear multiple times (EPAs)
SELECT day, slot->>'time' as time, array_agg(slot->>'subject') as subjects
FROM courses,
     LATERAL (
         SELECT 'monday' as day, jsonb_array_elements(schedule->'monday') as slot
         UNION ALL SELECT 'tuesday', jsonb_array_elements(schedule->'tuesday')
         UNION ALL SELECT 'wednesday', jsonb_array_elements(schedule->'wednesday')
         UNION ALL SELECT 'thursday', jsonb_array_elements(schedule->'thursday')
         UNION ALL SELECT 'friday', jsonb_array_elements(schedule->'friday')
     ) slots
WHERE name = '2do año 1era'
GROUP BY day, slot->>'time'
HAVING COUNT(*) > 1;
```

### List teacher assignments
```sql
SELECT cs.id, c.name as course, s.name as subject, u.name as teacher
FROM course_subjects cs
JOIN courses c ON cs.course_id = c.id
JOIN subjects s ON cs.subject_id = s.id
JOIN users u ON cs.teacher_id = u.id;
```

### List all categories with hierarchy
```sql
SELECT c.id, c.name, ka.name as knowledge_area, pn.name as nucleus
FROM categories c
JOIN knowledge_areas ka ON c.knowledge_area_id = ka.id
JOIN problematic_nuclei pn ON ka.nucleus_id = pn.id;
```

### List all proposals
```sql
SELECT id, name, description, duration_weeks, is_active FROM proposals;
```

### List proposal progress for a teacher
```sql
SELECT pp.id, p.name as proposal, cs.id as course_subject_id, pp.status, pp.started_at
FROM proposal_progress pp
JOIN proposals p ON pp.proposal_id = p.id
JOIN course_subjects cs ON pp.course_subject_id = cs.id
WHERE pp.user_id = 1;
```

---

## Quick Reference - Current IDs

### Areas (7)
| ID | Name |
|----|------|
| 1 | Cs. Sociales, Políticas y Económicas |
| 2 | Lenguajes y Producción Cultural |
| 3 | Ciencias Naturales |
| 4 | Matemática - Informática |
| 5 | Integración Tecnológica |
| 6 | EFI |
| 7 | ESI |

### Subjects by Area (18 total)
| ID | Subject | Area ID |
|----|---------|---------|
| 1 | Historia | 1 |
| 2 | Geografía | 1 |
| 3 | Economía | 1 |
| 4 | Construcción de Ciudadanías | 1 |
| 5 | Filosofía | 1 |
| 6 | Lengua | 2 |
| 7 | Literatura | 2 |
| 8 | Lenguas Otras (Inglés) | 2 |
| 9 | Artes Visuales | 2 |
| 10 | Comunicación y Medios | 2 |
| 11 | Lengua preexistente | 2 |
| 12 | Lengua y literatura | 2 |
| 13 | Biología | 3 |
| 14 | Química | 3 |
| 15 | Física | 3 |
| 16 | Matemática | 4 |
| 17 | Informática | 4 |
| 18 | Integración tecnológica | 5 |

### Categories (12)
| ID | Name |
|----|------|
| 1 | Tiempos/territorios |
| 2 | Subjetividad |
| 3 | Trabajos |
| 4 | Revolución |
| 5 | Estado |
| 6 | Acumulación |
| 7 | Naturaleza |
| 8 | Derechos |
| 9 | Ética |
| 10 | Necesidades |
| 11 | Satisfactores |
| 12 | Bienes Comunes |

---

## Important Notes

1. **Foreign key constraints**: Always verify that referenced IDs exist before inserting
2. **Schedule format**: Days must be lowercase: monday, tuesday, wednesday, thursday, friday
3. **EPAs (shared classes)**: Represented by multiple entries at the same time slot
4. **Disciplinary nuclei**: Stored in `subjects.description` for Area 1 subjects
5. **subjects_data keys**: Use subject_id as string keys (e.g., "1", "2")
6. **Status values**: coordination_documents use 'draft', 'published', 'archived'
7. **Array syntax**: Use PostgreSQL array syntax `'{1,2,3}'` for integer arrays
8. **Proposals are seeded**: Proposals come from `seeds/seed_proposals.sql` - edit there for permanent changes
9. **proposal_progress unique constraint**: One progress record per (user, proposal, course_subject) combination
