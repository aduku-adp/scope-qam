# scope-qam
SCOPE-QAM Case study project


1. Data Extraction & Ingestion: extraction
2. Data Modeling & Warehouse Design: dbt
3. Data Pipeline Orchestration: airflow
4. API Development with FastAPI: qam-api
5. Containerization & Infrastructure



## Running Airflow: Initializing Environment

- Setting the right Airflow user

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```


- Initialize airflow.cfg (Optional)

```bash
docker compose run airflow-cli airflow config list

```


- Initialize the database

```bash
docker compose up airflow-init
```



- Cleaning-up the environment

```bash
docker compose down --volumes --remove-orphans
```



- Running Airflow

```bash
docker compose up
```
