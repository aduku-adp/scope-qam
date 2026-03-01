-- One-time migration template:
-- Convert raw.rating_assessments_history to monthly RANGE partitioning on source_modified_at_utc.
-- Run during a maintenance window.

BEGIN;

CREATE TABLE IF NOT EXISTS raw.rating_assessments_history_p (
    LIKE raw.rating_assessments_history INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
) PARTITION BY RANGE (source_modified_at_utc);

-- Backfill existing data.
INSERT INTO raw.rating_assessments_history_p
SELECT *
FROM raw.rating_assessments_history;

-- Create an initial catch-all partition (replace with monthly partitions once stable).
CREATE TABLE IF NOT EXISTS raw.rating_assessments_history_default
PARTITION OF raw.rating_assessments_history_p DEFAULT;

-- Swap table names.
ALTER TABLE raw.rating_assessments_history RENAME TO rating_assessments_history_old;
ALTER TABLE raw.rating_assessments_history_p RENAME TO rating_assessments_history;

COMMIT;

-- Drop old table after validation:
-- DROP TABLE raw.rating_assessments_history_old;
