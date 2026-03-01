-- One-time migration template:
-- Convert facts.fct_company_timeseries to monthly RANGE partitioning on event_time.
-- Run after dbt models are materialized and during a maintenance window.

BEGIN;

CREATE TABLE IF NOT EXISTS facts.fct_company_timeseries_p (
    LIKE facts.fct_company_timeseries INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
) PARTITION BY RANGE (event_time);

INSERT INTO facts.fct_company_timeseries_p
SELECT *
FROM facts.fct_company_timeseries;

CREATE TABLE IF NOT EXISTS facts.fct_company_timeseries_default
PARTITION OF facts.fct_company_timeseries_p DEFAULT;

ALTER TABLE facts.fct_company_timeseries RENAME TO fct_company_timeseries_old;
ALTER TABLE facts.fct_company_timeseries_p RENAME TO fct_company_timeseries;

COMMIT;

-- Drop old table after validation:
-- DROP TABLE facts.fct_company_timeseries_old;
