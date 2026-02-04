from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Examination(Base):
    __tablename__ = "examinations"
    reg_number = Column(BigInteger, primary_key=True)
    student_id = Column(BigInteger)
    exam_type = Column(String)
    exam_year = Column(String)
    subject_name = Column(String)
    score = Column(BigInteger)
    grade = Column(String)
    center_id = Column(BigInteger)
    exam_center = Column(String)

class School(Base):
    __tablename__ = "schools"
    school_id = Column(BigInteger, primary_key=True)
    school_name = Column(String)
    state = Column(String)
    lga = Column(String)
    school_address = Column(String)
    school_type = Column(String)
    institution_level = Column(String)
    no_of_students = Column(BigInteger)
    no_of_teachers = Column(BigInteger)
    contact_info = Column(BigInteger)

class Student(Base):
    __tablename__ = "students"
    student_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(String)
    age = Column(BigInteger)
    state_of_origin = Column(String)
    state_of_residence = Column(String)
    student_email = Column(String)
    student_phone_no = Column(BigInteger)
    school_id = Column(BigInteger)
    parent_name = Column(String)
    parent_phone_no = Column(BigInteger)
    parent_email = Column(String)
    parent_address = Column(String)
    NIN = Column(BigInteger)

class Teacher(Base):
    __tablename__ = "teachers"
    teacher_id = Column(BigInteger, primary_key=True)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    age = Column(BigInteger)
    teacher_email = Column(String)
    teacher_phone_no = Column(BigInteger)
    school_id = Column(BigInteger)
    subject_taught = Column(String)
    trained_teacher = Column(Boolean)
    education_level = Column(String)
    years_of_experience = Column(BigInteger)
