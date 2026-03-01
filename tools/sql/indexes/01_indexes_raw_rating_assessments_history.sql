-- Indexes for raw.rating_assessments_history
-- Safe to re-run.
--
-- Note:
-- - On non-partitioned tables we keep unique indexes for dedup/version integrity.
-- - On partitioned tables Postgres requires unique indexes to include the partition key,
--   so we create non-unique lookup indexes instead.

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
        EXECUTE '
            CREATE INDEX IF NOT EXISTS idx_raw_rah_record_hash
            ON raw.rating_assessments_history (record_hash)
        ';
        EXECUTE '
            CREATE INDEX IF NOT EXISTS idx_raw_rah_company_doc
            ON raw.rating_assessments_history (company_id, document_version)
        ';
    ELSE
        EXECUTE '
            CREATE UNIQUE INDEX IF NOT EXISTS uq_raw_rah_record_hash
            ON raw.rating_assessments_history (record_hash)
        ';
        EXECUTE '
            CREATE UNIQUE INDEX IF NOT EXISTS uq_raw_rah_company_doc
            ON raw.rating_assessments_history (company_id, document_version)
        ';
    END IF;

    EXECUTE '
        CREATE INDEX IF NOT EXISTS idx_raw_rah_source_modified
        ON raw.rating_assessments_history (source_modified_at_utc DESC)
    ';
    EXECUTE '
        CREATE INDEX IF NOT EXISTS idx_raw_rah_company_source_modified
        ON raw.rating_assessments_history (company_id, source_modified_at_utc DESC)
    ';
    EXECUTE '
        CREATE INDEX IF NOT EXISTS idx_raw_rah_source_file_path
        ON raw.rating_assessments_history (source_file_path)
    ';
    EXECUTE '
        CREATE INDEX IF NOT EXISTS idx_raw_rah_ingested_at
        ON raw.rating_assessments_history (ingested_at DESC)
    ';
END
$$;
