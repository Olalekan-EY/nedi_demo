import requests
from decouple import config

# Load ClickHouse configuration from environment
CLICKHOUSE_HOST = config("CLICKHOUSE_HOST", default="localhost")
CLICKHOUSE_HTTP_PORT = config("CLICKHOUSE_HTTP_PORT", default="8123")
CLICKHOUSE_USER = config("CLICKHOUSE_USER", default="default")
CLICKHOUSE_PASSWORD = config("CLICKHOUSE_PASSWORD", default="yourpassword")

CLICKHOUSE_HTTP_URL = config("CLICKHOUSE_HTTP_URL", default=f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_HTTP_PORT}/")
AUTH = (CLICKHOUSE_USER, CLICKHOUSE_PASSWORD)


def run_clickhouse_query(query: str):
    """Send SQL query to ClickHouse."""
    response = requests.post(
        CLICKHOUSE_HTTP_URL,
        params={"query": query},
        auth=AUTH
    )
    if response.status_code != 200:
        raise Exception(f"ClickHouse Error: {response.text}") 
    return response.text


def create_database():
    run_clickhouse_query("CREATE DATABASE IF NOT EXISTS analytics")
    print("Database 'analytics' ready")


def create_examinations_table():
    query = """
    CREATE TABLE IF NOT EXISTS analytics.examinations (
        reg_number       Int64,
        student_id       Int64,
        exam_type        String,
        exam_year        String,
        subject_name     String,
        score            Int64,
        grade            String,
        center_id        Int64,
        exam_center      String
    )
    ENGINE = MergeTree()
    ORDER BY reg_number
    """
    run_clickhouse_query(query)
    print("Table 'examinations' ready")


def create_students_table():
    query = """
    CREATE TABLE IF NOT EXISTS analytics.students (
        student_id         Int64,
        first_name         String,
        last_name          String,
        gender             String,
        date_of_birth      String,
        age                Int64,
        state_of_origin    String,
        state_of_residence String,
        student_email      String,
        student_phone_no   Int64,
        school_id          Int64,
        parent_name        String,
        parent_phone_no    Int64,
        parent_email       String,
        parent_address     String,
        NIN                Int64
    )
    ENGINE = MergeTree()
    ORDER BY student_id
    """
    run_clickhouse_query(query)
    print("Table 'students' ready")


def create_schools_table():
    query = """
    CREATE TABLE IF NOT EXISTS analytics.schools (
        school_id         Int64,
        school_name       String,
        state             String,
        lga               String,
        school_address    String,
        school_type       String,
        institution_level String,
        no_of_students    Int64,
        no_of_teachers    Int64,
        contact_info      Int64
    )
    ENGINE = MergeTree()
    ORDER BY school_id
    """
    run_clickhouse_query(query)
    print("Table 'schools' ready")


def create_teachers_table():
    query = """
    CREATE TABLE IF NOT EXISTS analytics.teachers (
        teacher_id         Int64,
        title              String,
        first_name         String,
        last_name          String,
        date_of_birth      String,
        age                Int64,
        teacher_email      String,
        teacher_phone_no   Int64,
        school_id          Int64,
        subject_taught     String,
        trained_teacher    Bool,
        education_level    String,
        years_of_experience Int64
    )
    ENGINE = MergeTree()
    ORDER BY teacher_id
    """
    run_clickhouse_query(query)
    print("Table 'teachers' ready")


def init_clickhouse():
    print("Initializing ClickHouse...")

    create_database()
    create_examinations_table()
    create_students_table()
    create_schools_table()
    create_teachers_table()

    print("\nAll ClickHouse tables are ready!")


if __name__ == "__main__":
    init_clickhouse()
