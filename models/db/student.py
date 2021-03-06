from datetime import date
from collections import namedtuple
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, and_
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import literal, union
from models.dbcontext import DbContext as db
from models.db.grade import Grade
from models.db.course import Course
from models.db.field import Field
from models.db.occupation import Occupation
from models.db.studentsnapshot import StudentSnapshot

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
    snapshot = relationship("StudentSnapshot", uselist=False)

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
    def generate_all_snapshots(cls, session):
        """
        this will run as a batch process in the evenings
        to improve speed of daily requests;
        generating per student not per existing snapshot
        to account for students added between batches 
        """
        for student in cls.get_all(session):
            class_rank = cls.class_rank(session, student.grad_year, student.id)
            hist_rank = cls.historical_rank(session, student.id)
            strongest_sub = cls.strongest_sub(session, student.id)
            weakest_sub = cls.weakest_sub(session, student.id)
            if student.snapshot is None:
                student.snapshot = StudentSnapshot(student_id=student.id,
                                                   class_rank=class_rank,
                                                   hist_rank=hist_rank,
                                                   strongest_sub=strongest_sub,
                                                   weakest_sub=weakest_sub)
            else:
                student.snapshot.class_rank = class_rank
                student.snapshot.hist_rank = hist_rank
                student.snapshot.strongest_sub_id, student.snapshot.strongest_sub_avg = strongest_sub
                student.snapshot.weakest_sub_id, student.snapshot.weakest_sub_avg = weakest_sub
            cls.add(session, student)

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
        """
        returns (top 3) occupations and former students
        that most closely match the given student
        """
        # get current snapshot info
        student = cls.find_by_id(session, student_id)
        # used when filtering students by grad year
        # d = date.today()
        # dummy grad date for testing
        d = date(2023, 1, 1)
        # get all former students with a gpa within +-.05 of student
        gpa_q = session.query(cls.id.label("sid"),
                              cls.occupation_id.label("oid"),
                              literal(3).label("sim_score")).\
                filter(cls.grad_year < d.year).\
                filter(and_(cls.gpa >= (student.gpa - .05), cls.gpa <= (student.gpa + .05)))
        # get all former students whose strongest subject is same as student
        strongest_sub_q = session.query(cls.id.label("sid"),
                                        cls.occupation_id.label("oid"),
                                        literal(2).label("sim_score")).\
                          join(StudentSnapshot).\
                          filter(cls.grad_year < d.year).\
                          filter(StudentSnapshot.strongest_sub_id == student.snapshot.strongest_sub_id)
        # get all former students whose weakest subject is same as student
        weakest_sub_q = session.query(cls.id.label("sid"),
                                      cls.occupation_id.label("oid"),
                                      literal(1).label("sim_score")).\
                        join(StudentSnapshot).\
                        filter(cls.grad_year < d.year).\
                        filter(StudentSnapshot.weakest_sub_id == student.snapshot.weakest_sub_id)
        # union of above 3 queries
        fit_values = union(gpa_q, strongest_sub_q, weakest_sub_q).alias("fit_values")
        sum_func = func.sum(fit_values.c.sim_score).label("total_score")
        # get top 3 students with highest similarity score
        top_students = session.query(fit_values.c.sid, sum_func).\
                       group_by(fit_values.c.sid).\
                       order_by(sum_func.desc()).\
                       limit(3).\
                       all()
        # get top 3 occupations with highest similarity score
        top_occupations = session.query(fit_values.c.oid, sum_func).\
                          group_by(fit_values.c.oid).\
                          order_by(sum_func.desc()).\
                          limit(3).\
                          all()
        
        return (top_students, top_occupations)

    @classmethod
    def strongest_sub(cls, session, student_id: int):
        avg_func = func.avg(Grade.grade).label("avg_grade")
        subq = session.query(cls.id, Field.id.label("field_id"), avg_func).\
               join(Grade).\
               join(Course).\
               join(Field).\
               filter(cls.id == student_id).\
               group_by(cls.id, Field.id).\
               subquery()
        
        max_func = func.max(subq.c.avg_grade).label("max_avg_grade")
        maxsub = session.query(subq.c.field_id, max_func).\
                 group_by(subq.c.field_id).\
                 order_by(max_func.desc())
        return maxsub.first()
    
    @classmethod
    def weakest_sub(cls, session, student_id: int):
        avg_func = func.avg(Grade.grade).label("avg_grade")
        subq = session.query(cls.id, Field.id.label("field_id"), avg_func).\
               join(Grade).\
               join(Course).\
               join(Field).\
               filter(cls.id == student_id).\
               group_by(cls.id, Field.id).\
               subquery()
        
        min_func = func.min(subq.c.avg_grade).label("min_avg_grade")
        minsub = session.query(subq.c.field_id, min_func).\
                 group_by(subq.c.field_id).\
                 order_by(min_func)
        return minsub.first()

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
