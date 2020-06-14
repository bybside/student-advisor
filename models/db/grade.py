from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class Grade(db.Base):
    """
    model class (maps to grade table);
    associative entity between student and course tables
    """
    __tablename__ = "grade"

    grade = Column(Integer)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    student = relationship("Student")
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
    course = relationship("Course")

    def __init__(self, grade, student_id, course_id):
        self.grade = grade
        self.student_id = student_id
        self.course_id = course_id
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @property
    def serialize(self):
        """
        needed to make Grade objects JSON serializable
        """
        return {
            "grade": self.grade,
            "student": {
                "id": self.student_id,
                "fname": self.student.fname,
                "lname": self.student.lname,
                "dob": self.student.dob,
                "grad_year": self.student.grad_year,
                "gpa": self.student.gpa,
                "occupation": self.student.occupation.serialize
            },
            "course": {
                "id": self.course_id,
                "course_name": self.course.course_name,
                "field": self.course.field.serialize,
                "faculty": self.course.faculty.serialize,
                "semester": self.course.semester.serialize
            }
        }
    
    def __repr__(self):
        return f"Grade({self.grade}, {self.student}, {self.course})"
