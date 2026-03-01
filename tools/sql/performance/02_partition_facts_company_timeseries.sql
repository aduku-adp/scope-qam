-- Idempotent migration:
-- Convert facts.fct_company_timeseries to RANGE partitioning on event_time.
-- Safe to re-run after completion.

DO $$
DECLARE
    table_is_partitioned boolean;
BEGIN
    IF to_regclass('facts.fct_company_timeseries') IS NULL THEN
        RAISE NOTICE 'facts.fct_company_timeseries does not exist. Skipping.';
        RETURN;
    END IF;

    SELECT EXISTS (
        SELECT 1
        FROM pg_partitioned_table p
        JOIN pg_class c ON c.oid = p.partrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'facts'
          AND c.relname = 'fct_company_timeseries'
    )
    INTO table_is_partitioned;

    IF table_is_partitioned THEN
        RAISE NOTICE 'facts.fct_company_timeseries is already partitioned. Skipping.';
        RETURN;
    END IF;

    IF to_regclass('facts.fct_company_timeseries_p') IS NULL THEN
        EXECUTE '
            CREATE TABLE facts.fct_company_timeseries_p (
                LIKE facts.fct_company_timeseries INCLUDING DEFAULTS
            ) PARTITION BY RANGE (event_time)
        ';
    END IF;

    IF to_regclass('facts.fct_company_timeseries_default') IS NULL THEN
        EXECUTE '
            CREATE TABLE facts.fct_company_timeseries_default
            PARTITION OF facts.fct_company_timeseries_p DEFAULT
        ';
    END IF;

    EXECUTE 'TRUNCATE TABLE facts.fct_company_timeseries_p';
    EXECUTE '
        INSERT INTO facts.fct_company_timeseries_p
        SELECT *
        FROM facts.fct_company_timeseries
    ';

    IF to_regclass('facts.fct_company_timeseries_old') IS NULL THEN
        EXECUTE 'ALTER TABLE facts.fct_company_timeseries RENAME TO fct_company_timeseries_old';
        EXECUTE 'ALTER TABLE facts.fct_company_timeseries_p RENAME TO fct_company_timeseries';
    ELSE
        RAISE NOTICE 'facts.fct_company_timeseries_old already exists; swap already executed or partially applied.';
    END IF;
END
$$;

-- Drop old table after validation:
-- DROP TABLE facts.fct_company_timeseries_old;
