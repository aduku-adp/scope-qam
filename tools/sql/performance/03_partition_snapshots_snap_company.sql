-- One-time migration template:
-- Convert snapshots.snap_company to monthly RANGE partitioning on dbt_valid_from.
-- Run after dbt snapshot model is created and during a maintenance window.

BEGIN;

CREATE TABLE IF NOT EXISTS snapshots.snap_company_p (
    LIKE snapshots.snap_company INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
) PARTITION BY RANGE (dbt_valid_from);

INSERT INTO snapshots.snap_company_p
SELECT *
FROM snapshots.snap_company;

CREATE TABLE IF NOT EXISTS snapshots.snap_company_default
PARTITION OF snapshots.snap_company_p DEFAULT;

ALTER TABLE snapshots.snap_company RENAME TO snap_company_old;
ALTER TABLE snapshots.snap_company_p RENAME TO snap_company;

COMMIT;

-- Drop old table after validation:
-- DROP TABLE snapshots.snap_company_old;
