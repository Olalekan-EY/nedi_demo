from sqlalchemy.orm import  Session
from fast_api.models import *

class AppDao:
    def __init__(self, db:Session):
        self.db = db
    
    def get_examinations(self):
        return self.db.query(Examination).all()
    
    def get_teachers(self):
        return self.db.query(Teacher).all()
    
    def get_students(self):
        return self.db.query(Student).all()
    
    def get_schools(self):
        return self.db.query(School).all()