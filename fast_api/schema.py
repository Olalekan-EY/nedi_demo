from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from fast_api.models import Examination, School, Student, Teacher

ExaminationRead = sqlalchemy_to_pydantic(Examination)
SchoolRead = sqlalchemy_to_pydantic(School)
StudentRead = sqlalchemy_to_pydantic(Student)
TeacherRead = sqlalchemy_to_pydantic(Teacher)

