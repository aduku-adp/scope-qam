# AI Usage Disclosure

## Tools used

- ChatGPT / Codex-style assistant (this repository work session)

## Components that received AI assistance

- `modules/data-extraction`
  - pipeline orchestration changes
  - validation/business-rule wiring
  - observability table integration
- `modules/dbt_qam`
  - marts/snapshots SQL model iterations
- `modules/qam-api`
  - company/snapshot/upload/health endpoints
  - provider/service/controller/tests
- `modules/airflow/dags`
  - DAG creation and task-chain updates
- `docker-compose.yaml`
  - service wiring, ports, health checks, mounts
- documentation (`README.md`)

## Nature of assistance

- Drafting/refactoring Python and SQL code
- Suggesting schema/modeling patterns
- Generating tests and fixing test failures
- Writing operational scripts and API docs examples

## Human review and validation

- All generated code was manually reviewed and edited in-repo.
- Final behavior was validated with local test runs, dbt runs, and endpoint checks.

## Chat logs / screenshots

- AI interaction logs are available in the coding assistant conversation history for this assignment session.
- Sensitive values were not intentionally included in prompts.

