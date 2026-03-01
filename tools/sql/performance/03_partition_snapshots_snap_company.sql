-- Idempotent migration:
-- Convert snapshots.snap_company to RANGE partitioning on dbt_valid_from.
-- Safe to re-run after completion.

DO $$
DECLARE
    table_is_partitioned boolean;
BEGIN
    IF to_regclass('snapshots.snap_company') IS NULL THEN
        RAISE NOTICE 'snapshots.snap_company does not exist. Skipping.';
        RETURN;
    END IF;

    SELECT EXISTS (
        SELECT 1
        FROM pg_partitioned_table p
        JOIN pg_class c ON c.oid = p.partrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'snapshots'
          AND c.relname = 'snap_company'
    )
    INTO table_is_partitioned;

    IF table_is_partitioned THEN
        RAISE NOTICE 'snapshots.snap_company is already partitioned. Skipping.';
        RETURN;
    END IF;

    IF to_regclass('snapshots.snap_company_p') IS NULL THEN
        EXECUTE '
            CREATE TABLE snapshots.snap_company_p (
                LIKE snapshots.snap_company INCLUDING DEFAULTS
            ) PARTITION BY RANGE (dbt_valid_from)
        ';
    END IF;

    IF to_regclass('snapshots.snap_company_default') IS NULL THEN
        EXECUTE '
            CREATE TABLE snapshots.snap_company_default
            PARTITION OF snapshots.snap_company_p DEFAULT
        ';
    END IF;

    EXECUTE 'TRUNCATE TABLE snapshots.snap_company_p';
    EXECUTE '
        INSERT INTO snapshots.snap_company_p
        SELECT *
        FROM snapshots.snap_company
    ';

    IF to_regclass('snapshots.snap_company_old') IS NULL THEN
        EXECUTE 'ALTER TABLE snapshots.snap_company RENAME TO snap_company_old';
        EXECUTE 'ALTER TABLE snapshots.snap_company_p RENAME TO snap_company';
    ELSE
        RAISE NOTICE 'snapshots.snap_company_old already exists; swap already executed or partially applied.';
    END IF;
END
$$;

-- Drop old table after validation:
-- DROP TABLE snapshots.snap_company_old;
