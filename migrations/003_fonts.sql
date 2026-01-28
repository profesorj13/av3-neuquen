-- Fonts table for validated documents/resources
CREATE TABLE IF NOT EXISTS fonts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    thumbnail_url TEXT,
    area_id INTEGER REFERENCES areas(id),
    is_validated BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add new columns to teacher_lesson_plans
ALTER TABLE teacher_lesson_plans
ADD COLUMN IF NOT EXISTS custom_instruction TEXT,
ADD COLUMN IF NOT EXISTS resources_mode VARCHAR(20) DEFAULT 'global',
ADD COLUMN IF NOT EXISTS global_font_id INTEGER REFERENCES fonts(id),
ADD COLUMN IF NOT EXISTS moment_font_ids JSONB;

CREATE INDEX IF NOT EXISTS idx_fonts_area ON fonts(area_id);
CREATE INDEX IF NOT EXISTS idx_fonts_validated ON fonts(is_validated);
