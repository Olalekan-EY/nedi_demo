from dagster import ScheduleDefinition, DefaultScheduleStatus
from job import sync_to_clickhouse

sync_to_clickhouse_schedule = ScheduleDefinition(
    name="sync_to_clickhouse_schedule",
    job=sync_to_clickhouse,
    cron_schedule="0 */6 * * *",
    default_status=DefaultScheduleStatus.RUNNING,
    description="Schedule to sync data from PostgreSQL to ClickHouse. The cron schedule can be modified directly in the Dagster UI under Schedules."
)
