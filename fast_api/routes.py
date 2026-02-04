from fastapi import APIRouter, Request, Depends
from fast_api.db import get_db
from fast_api.dao import AppDao
from sqlalchemy.orm import Session
import requests
from fast_api.schema import ExaminationRead, SchoolRead, StudentRead, TeacherRead
from fast_api.config import CLICKHOUSE_HTTP_URL, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD

router = APIRouter()

AUTH = (CLICKHOUSE_USER, CLICKHOUSE_PASSWORD)

# Mapping DAO methods to ClickHouse tables
TABLE_MAPPING = {
    "examinations": "analytics.examinations",
    "teachers": "analytics.teachers",
    "students": "analytics.students",
    "schools": "analytics.schools"
}

def get_app_dao(db:Session = Depends(get_db)) -> AppDao:
    return AppDao(db)


def push_to_clickhouse(table_name: str, records: list):
    """Generic function to push records to ClickHouse"""
    if not records:
        return {"status": "empty", "detail": f"No records to insert into {table_name}"}

    url = f"{CLICKHOUSE_HTTP_URL}?query=INSERT INTO {table_name} FORMAT JSONEachRow"

    response = requests.post(
        url,
        json=records,
        auth=AUTH,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return {"status": "success", "inserted": len(records)}
    else:
        return {"status": "error", "detail": response.text}


@router.get("/examinations")
def get_examinations(
    request:Request,
    dao:AppDao = Depends(get_app_dao)
):
     return {
         "data": dao.get_examinations()
     }
     
     
@router.get("/teachers")
def get_teachers(
    request:Request,
    dao:AppDao = Depends(get_app_dao)
):
     return {
         "data": dao.get_teachers()
     }
     

@router.get("/schools")
def get_schools(
    request:Request,
    dao:AppDao = Depends(get_app_dao)
):
     return {
         "data": dao.get_schools()
     }
     
@router.get("/students")
def get_students(
    request:Request,
    dao:AppDao = Depends(get_app_dao)
):
     return {
         "data": dao.get_students()
     }


@router.post("/examinations/clickhouse")
def push_examinations(dao: AppDao = Depends(get_app_dao)):
    records = dao.get_examinations()
    data = [ExaminationRead.from_orm(record).dict() for record in records]
    return push_to_clickhouse(TABLE_MAPPING["examinations"], data)


@router.post("/teachers/clickhouse")
def push_teachers(dao: AppDao = Depends(get_app_dao)):
    records = dao.get_teachers()
    data = [TeacherRead.from_orm(record).dict() for record in records]
    return push_to_clickhouse(TABLE_MAPPING["teachers"], data)


@router.post("/students/clickhouse")
def push_students(dao: AppDao = Depends(get_app_dao)):
    records = dao.get_students()
    data = [StudentRead.from_orm(record).dict() for record in records]
    return push_to_clickhouse(TABLE_MAPPING["students"], data)


@router.post("/schools/clickhouse")
def push_schools(dao: AppDao = Depends(get_app_dao)):
    records = dao.get_schools()
    data = [SchoolRead.from_orm(record).dict() for record in records]
    return push_to_clickhouse(TABLE_MAPPING["schools"], data)

