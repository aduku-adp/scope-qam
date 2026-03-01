# Chat History Export (Assistant-side)

This file captures the full assistant-side working history for this session as a structured export.

## Note

- This is not the platform-native raw transcript export format.
- It is a reconstructed, comprehensive session log of user requests and implemented actions.

## Session Timeline (Condensed but complete)

1. Built extraction pipeline for Excel MASTER sheet to JSON and Postgres target table.
2. Restricted extraction to MASTER sheet and made sheet name configurable/global.
3. Switched file IO behavior to read from `./data` and then DB-only mode.
4. Aligned extraction output shape to expected nested JSON model (A_2 expectations).
5. Moved `segmentation_criteria` under `industry_risk` then into `company_information` model updates.
6. Designed and updated raw table model; renamed target table to `raw.rating_assessments_history`.
7. Removed CLI args; ingestion from data directory only.
8. Added dedup strategy discussion and implemented `record_hash` behavior.
9. Fixed openpyxl `BadZipFile` path/data issues handling.
10. Added pytest unit tests and CI workflow; added Ruff checks in CI.
11. Refactored code location to `modules/data-extraction`, moved tests accordingly.
12. Proposed and implemented dbt star model: staging, dims, facts, bridges.
13. Resolved dbt run “successful but nothing written” understanding (schema targets/materializations).
14. Added metadata/lineage improvements in ingestion; migrated JSON blocks to JSONB.
15. Fixed psycopg2 insert argument formatting mismatch.
16. Removed version_info/lineage blocks per request and adjusted schema expectations.
17. Removed legacy columns (`document_version`, `extracted_at`, `source_system`, later `assessment_date`).
18. Updated dbt models accordingly (no unnecessary JSONB casts in staging).
19. Added strict schema validation with Pydantic; modularized extraction code.
20. Added run metrics logging and DB persistence in sys tables, then renamed/adjusted metrics and table names.
21. Added file-level status logging table and refined warning/error counting semantics.
22. Implemented entity/company versioning based on key and document version increments.
23. Implemented incremental load ordering and cutoff by `source_modified_at_utc`.
24. Strengthened strict primitive type validation (numeric/text/date).
25. Refactored extraction module into classes/modules for readability.
26. Added rounding to credit metric values (3 decimals).
27. Added extraction/validation/load failure counters.
28. Updated dbt for upstream schema/logic changes.
29. Fixed dbt SQL syntax issues and removed obsolete fields from transformations.
30. Implemented company SCD behavior in dbt (`start_at`, `end_at`, `is_active`).
31. Renamed entity -> company naming across models/API.
32. Merged methodology + industry risk into company information/model.
33. Fixed ingestion SQL references after column rename (`entity_*` -> `company_*`).
34. Added `document_version` to `dim_company` and handled multi-version behavior.
35. Assisted Docker/Airflow issues (ARM image manifests, airflow version/init issues, profiles path, hostnames).
36. Added local/airflow dbt profile targets (`dev`, `airflow`).
37. Updated Postgres init SQL for airflow DB/user creation.
38. Added deployment scripts and consolidated build/deploy behavior.
39. Added daily Airflow DAG sequence: extract -> dbt run -> dbt test (+snapshot flow later).
40. Resolved Airflow task runtime DB host/profile issues in containers.
41. Implemented business-rule engine (YAML-driven), removed SQL-rule layer on request.
42. Added support for `industry_risk` list pattern and corresponding dbt models/bridges.
43. Reviewed input file patterns and incorporated handling/validation updates.
44. Restored/propagated `segmentation_criteria` into storage/model/dbt outputs.
45. Gitignore guidance for local Postgres data directory.
46. Expanded observability table design and implemented requested observability capabilities.
47. Removed legacy `sys.file_logs`/`sys.run_logs` from pipeline and printed pipeline run event output.
48. Updated qam-api provider tests to align with provider changes.
49. Reworked qam-api structure compatibility and fixed import/type issues (`psycopg2.rows`, typing/list subscripting, etc.).
50. Fixed controller tests for not-found handling and FastAPI deprecation usage.
51. Renamed tests in data-extraction to suffix style (`*_test.py`).
52. Enabled/adjusted qam-api e2e tests and route expectations.
53. Updated qam-api Dockerfile base image support and build scripts.
54. Added qam-api service block in compose and local build script integration.
55. Implemented company compare diffs output and corrected model validation around mixed data types.
56. Added/updated company history filters (`column_name`, `metric_name`, `year_label`) and tests.
57. Built unified `facts.fct_company_timeseries` for history endpoint.
58. Implemented snapshot endpoints and later switched to dbt built-in snapshots.
59. Fixed snapshot endpoint/runtime errors and output schema alignment.
60. Ensured latest/active joins and max-version logic in snapshot/reporting models.
61. Added separate snapshot DAG and removed snapshot run from main DAG, then reintroduced combined testing strategy per request.
62. Renamed DAG `ratings_etl_pipeline` -> `company_etl_pipeline`.
63. Implemented upload audit endpoints end-to-end.
64. Moved corporate files to `data/corporates` and updated mounts/paths.
65. Performed assignment gap review and implemented missing items requested.
66. Added exponential backoff retry in ingestion pipeline.
67. Renamed extraction entrypoint to `extract_company_history` and class `CompanyExtractionPipeline`.
68. Added reports layer `reports.rep_company`; switched company endpoints to this source (history remains timeseries source).
69. Removed selected keys from endpoint outputs and compare payload as requested.
70. Updated comparison logic to compare all rep_company columns except excluded identifiers.
71. Added architecture and documentation improvements across modules.
72. Standardized README links (absolute -> repo-relative -> root-relative) per instructions.
73. Added architecture diagram references and image usage updates.
74. Renamed `build-airflow.sh` -> `build_airflow.sh` and updated references.
75. Added `build_qam_api.sh` usage in deploy scripts.
76. Updated startup docs to use `tools/clean_deploy_stack.sh` as one-command startup.
77. Reformatted root README API sample section into request/response blocks.
78. Adapted Postgres initialization approach:
   - Reverted compose sidecar schema-init.
   - Added `tools/postgres-init/02-create-qam-schemas.sql` to run after `01-create-airflow-db.sql`.
79. Added partition execution script `tools/create_partitions.sh` and integrated it into clean deploy.
80. Made partition SQL scripts idempotent and fixed default-partition load order.
81. Renamed `tools/sql/performance` -> `tools/sql/partitions` and updated references.
82. Added indexing scripts under `tools/sql/indexes` for raw + obs schemas.
83. Added `tools/create_indexes.sh` to apply all index scripts.
84. Fixed raw index script for partitioned table compatibility and idempotency.

## Current Key Artifacts Added/Changed (High-level)

- Extraction module: `modules/data-extraction/*`
- API module: `modules/qam-api/*`
- dbt module: `modules/dbt_qam/*`
- Airflow DAGs: `modules/airflow/dags/*`
- Deployment scripts: `tools/*.sh`
- SQL init and optimization scripts:
  - `tools/postgres-init/*`
  - `tools/sql/partitions/*`
  - `tools/sql/indexes/*`
- Documentation:
  - root `README.md`
  - module READMEs
  - architecture docs/images
