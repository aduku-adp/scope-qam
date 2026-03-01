-- Indexes for observability tables in obs schema.
-- Safe to re-run.

-- obs.pipeline_runs
CREATE INDEX IF NOT EXISTS idx_obs_pipeline_runs_name_started
ON obs.pipeline_runs (pipeline_name, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_obs_pipeline_runs_status_started
ON obs.pipeline_runs (status, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_obs_pipeline_runs_started
ON obs.pipeline_runs (started_at DESC);

-- obs.file_ingestion_events
CREATE INDEX IF NOT EXISTS idx_obs_file_ingestion_events_ingested
ON obs.file_ingestion_events (ingested_at DESC, event_id DESC);

CREATE INDEX IF NOT EXISTS idx_obs_file_ingestion_events_run
ON obs.file_ingestion_events (run_id);

CREATE INDEX IF NOT EXISTS idx_obs_file_ingestion_events_status
ON obs.file_ingestion_events (status);

CREATE INDEX IF NOT EXISTS idx_obs_file_ingestion_events_source_modified
ON obs.file_ingestion_events (source_modified_at_utc DESC);

CREATE INDEX IF NOT EXISTS idx_obs_file_ingestion_events_source_file
ON obs.file_ingestion_events (source_file_path);

-- obs.data_quality_rule_results
CREATE INDEX IF NOT EXISTS idx_obs_dq_results_event_created
ON obs.data_quality_rule_results (event_id, created_at);

CREATE INDEX IF NOT EXISTS idx_obs_dq_results_run_created
ON obs.data_quality_rule_results (run_id, created_at);

CREATE INDEX IF NOT EXISTS idx_obs_dq_results_rule
ON obs.data_quality_rule_results (rule_id, status, created_at DESC);

-- obs.lineage_events
CREATE INDEX IF NOT EXISTS idx_obs_lineage_events_event_created
ON obs.lineage_events (event_id, created_at);

CREATE INDEX IF NOT EXISTS idx_obs_lineage_events_run_created
ON obs.lineage_events (run_id, created_at);

CREATE INDEX IF NOT EXISTS idx_obs_lineage_events_target_table_row
ON obs.lineage_events (target_table, target_row_id);

-- obs.pipeline_state
CREATE INDEX IF NOT EXISTS idx_obs_pipeline_state_last_success
ON obs.pipeline_state (last_successful_run_at DESC);

CREATE INDEX IF NOT EXISTS idx_obs_pipeline_state_max_source_modified
ON obs.pipeline_state (max_source_modified_at_utc DESC);

-- obs.processed_files
CREATE INDEX IF NOT EXISTS idx_obs_processed_files_last_run
ON obs.processed_files (last_run_id);

CREATE INDEX IF NOT EXISTS idx_obs_processed_files_source_modified
ON obs.processed_files (source_modified_at_utc DESC);

CREATE INDEX IF NOT EXISTS idx_obs_processed_files_source_file
ON obs.processed_files (source_file_path);

