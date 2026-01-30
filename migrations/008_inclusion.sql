-- Inclusion module tables

CREATE TABLE ramps (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(255),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    ramp_id INTEGER NOT NULL REFERENCES ramps(id),
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT,
    qr_code VARCHAR(100) UNIQUE,
    how_to_use TEXT,
    recommendations TEXT,
    rationale TEXT,
    classroom_benefit TEXT,
    needs_description TEXT,
    evaluation_criteria TEXT,
    quantity INTEGER DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE student_inclusion_profiles (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    is_transitory BOOLEAN DEFAULT FALSE,
    difficulties TEXT[] NOT NULL DEFAULT '{}',
    free_description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(student_id)
);
