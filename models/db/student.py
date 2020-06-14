from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db
from models.db.grade import Grade
from models.db.course import Course
from models.db.field import Field
from models.db.occupation import Occupation

class Student(db.Base):
    """
    model class (maps to student table)
    """
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    dob = Column(Date)
    grad_year = Column(Integer)
    gpa = Column(Float)
    occupation_id = Column(Integer, ForeignKey("occupation.id"))
    occupation = relationship("Occupation")
    grades = relationship("Grade")

    def __init__(self, fname, lname, dob, grad_year, gpa, occupation_id):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.grad_year = grad_year
        self.gpa = gpa
        self.occupation_id = occupation_id
    
    @staticmethod
    def add(session, student):
        session.add(student)
    
    @staticmethod
    def delete(session, student):
        session.delete(student)

    @classmethod
    def class_rank(cls, session, grad_year: int, student_id: int):
        rank_func = func.rank().\
                    over(order_by=cls.gpa.desc()).\
                    label("rank")
        grad_class_ranked = session.query(cls, rank_func).\
                            filter_by(grad_year=grad_year).\
                            subquery()
        rank = session.query(grad_class_ranked.c.rank).\
               filter(grad_class_ranked.c.id == student_id)
        return rank.scalar()

    @classmethod
    def historical_rank(cls, session, student_id: int):
        rank_func = func.rank().\
                    over(order_by=cls.gpa.desc()).\
                    label("rank")
        students_ranked = session.query(cls, rank_func).\
                          subquery()
        rank = session.query(students_ranked.c.rank).\
               filter(students_ranked.c.id == student_id)
        return rank.scalar()

    @classmethod
    def career_fit(cls, session, student_id: int):
        pass

    @classmethod
    def strongest_sub(cls, session, student_id: int):
        avg_func = func.avg(Grade.grade).label("avg_grade")
        subq = session.query(cls.id, Field.field_name, Field.area, avg_func).\
               join(Grade).\
               join(Course).\
               join(Field).\
               filter(cls.id == student_id).\
               group_by(cls.id, Field.field_name, Field.area).\
               subquery()
        
        max_func = func.max(subq.c.avg_grade).label("max_avg_grade")
        maxsub = session.query(subq.c.field_name, subq.c.area, max_func).\
                 group_by(subq.c.field_name, subq.c.area)
        return maxsub.one()
    
    @classmethod
    def weakest_sub(cls, session, student_id: int):
        avg_func = func.avg(Grade.grade).label("avg_grade")
        subq = session.query(cls.id, Field.field_name, Field.area, avg_func).\
               join(Grade).\
               join(Course).\
               join(Field).\
               filter(cls.id == student_id).\
               group_by(cls.id, Field.field_name, Field.area).\
               subquery()
        
        min_func = func.min(subq.c.avg_grade).label("min_avg_grade")
        minsub = session.query(subq.c.field_name, subq.c.area, min_func).\
                 group_by(subq.c.field_name, subq.c.area)
        return minsub.one()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, student_id: int):
        query = session.query(cls).filter_by(id=student_id)
        return query.one()

    @classmethod
    def find_by_grad_year(cls, session, grad_year: int):
        query = session.query(cls).filter_by(grad_year=grad_year)
        return query.all()

    @property
    def serialize(self):
        """
        needed to make Student objects JSON serializable
        """
        return {
            "id": self.id,
            "fname": self.fname,
            "lname": self.lname,
            "dob": self.dob,
            "grad_year": self.grad_year,
            "gpa": self.gpa,
            "occupation": self.occupation.serialize,
            "grades": [
                {
                    "grade": g.grade,
                    "course": {
                        "id": g.course.id,
                        "course_name": g.course.course_name,
                        "field": g.course.field.serialize,
                        "faculty": g.course.faculty.serialize,
                        "semester": g.course.semester.serialize
                    }
                } for g in self.grades
            ]
        }
    
    def __repr__(self):
        return f"Student({self.id}, {self.fname}, {self.lname}, {self.dob}, {self.grad_year}, {self.gpa}, {self.occupation}, {self.courses})"
