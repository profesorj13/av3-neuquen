-- Add new fields to coordination_documents for enhanced AI generation

-- Add problem_edge field (AI-generated problem statement)
ALTER TABLE coordination_documents ADD COLUMN IF NOT EXISTS problem_edge TEXT DEFAULT '';

-- Add eval_criteria field (AI-generated evaluation criteria)
ALTER TABLE coordination_documents ADD COLUMN IF NOT EXISTS eval_criteria TEXT DEFAULT '';

-- Convert methodological_strategies from TEXT to JSONB {type, context}
-- Strategy types: proyecto, taller_laboratorio, ateneo_debate
ALTER TABLE coordination_documents
  ALTER COLUMN methodological_strategies TYPE JSONB
  USING CASE
    WHEN methodological_strategies IS NULL THEN NULL
    WHEN methodological_strategies = '' THEN NULL
    ELSE jsonb_build_object('type', 'proyecto', 'context', methodological_strategies)
  END;
