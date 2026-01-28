-- Add moment_type column to activities table
ALTER TABLE activities ADD COLUMN IF NOT EXISTS moment_type VARCHAR(50);

-- Create index for filtering by moment_type
CREATE INDEX IF NOT EXISTS idx_activities_moment_type ON activities(moment_type);

-- Clear old activities to replace with new structured activities
DELETE FROM activities;
