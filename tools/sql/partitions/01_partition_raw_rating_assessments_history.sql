-- Idempotent migration:
-- Convert raw.rating_assessments_history to RANGE partitioning on source_modified_at_utc.
-- Safe to re-run after completion.

DO $$
DECLARE
    table_is_partitioned boolean;
BEGIN
    IF to_regclass('raw.rating_assessments_history') IS NULL THEN
        RAISE NOTICE 'raw.rating_assessments_history does not exist. Skipping.';
        RETURN;
    END IF;

    SELECT EXISTS (
        SELECT 1
        FROM pg_partitioned_table p
        JOIN pg_class c ON c.oid = p.partrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'raw'
          AND c.relname = 'rating_assessments_history'
    )
    INTO table_is_partitioned;

    IF table_is_partitioned THEN
        RAISE NOTICE 'raw.rating_assessments_history is already partitioned. Skipping.';
        RETURN;
    END IF;

    IF to_regclass('raw.rating_assessments_history_p') IS NULL THEN
        EXECUTE '
            CREATE TABLE raw.rating_assessments_history_p (
                LIKE raw.rating_assessments_history INCLUDING DEFAULTS
            ) PARTITION BY RANGE (source_modified_at_utc)
        ';
    END IF;

    IF to_regclass('raw.rating_assessments_history_default') IS NULL THEN
        EXECUTE '
            CREATE TABLE raw.rating_assessments_history_default
            PARTITION OF raw.rating_assessments_history_p DEFAULT
        ';
    END IF;

    -- Make pre-swap reruns deterministic.
    EXECUTE 'TRUNCATE TABLE raw.rating_assessments_history_p';
    EXECUTE '
        INSERT INTO raw.rating_assessments_history_p
        SELECT *
        FROM raw.rating_assessments_history
    ';

    IF to_regclass('raw.rating_assessments_history_old') IS NULL THEN
        EXECUTE 'ALTER TABLE raw.rating_assessments_history RENAME TO rating_assessments_history_old';
        EXECUTE 'ALTER TABLE raw.rating_assessments_history_p RENAME TO rating_assessments_history';
    ELSE
        RAISE NOTICE 'raw.rating_assessments_history_old already exists; swap already executed or partially applied.';
    END IF;
END
$$;

-- Drop old table after validation:
-- DROP TABLE raw.rating_assessments_history_old;
