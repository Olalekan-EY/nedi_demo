from dagster import Definitions
from job import sync_to_clickhouse, run_dbt_transformations, execute_data_pipeline
from schedule import sync_to_clickhouse_schedule

defs = Definitions(
    jobs=[sync_to_clickhouse, run_dbt_transformations, execute_data_pipeline],
    schedules=[sync_to_clickhouse_schedule]
)
