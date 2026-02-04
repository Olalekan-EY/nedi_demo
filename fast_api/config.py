from decouple import config

# PostgreSQL Configuration
POSTGRES_USER = config("POSTGRES_USER", default="myuser")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="mypassword")
POSTGRES_DB = config("POSTGRES_DB", default="nedi")
POSTGRES_HOST = config("POSTGRES_HOST", default="postgres")
POSTGRES_PORT = config("POSTGRES_PORT", default="5432", cast=int)

# ClickHouse Configuration
CLICKHOUSE_HOST = config("CLICKHOUSE_HOST", default="clickhouse")
CLICKHOUSE_PORT = config("CLICKHOUSE_PORT", default="9000", cast=int)
CLICKHOUSE_USER = config("CLICKHOUSE_USER", default="default")
CLICKHOUSE_PASSWORD = config("CLICKHOUSE_PASSWORD", default="yourpassword")
CLICKHOUSE_HTTP_URL = config("CLICKHOUSE_HTTP_URL", default=f"http://{CLICKHOUSE_HOST}:8123")

# Database URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

