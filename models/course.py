from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class Course(db.Base):
    """
    model class (maps to course table)
    """
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    field_id = Column(Integer, ForeignKey("field.id"))
    field = relationship("Field")
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    faculty = relationship("Faculty")
    semester_id = Column(Integer, ForeignKey("semester.id"))
    semester = relationship("Semester")
    grades = relationship("Grade")

    def __init__(self, course_name, field_id, faculty_id, semester_id):
        self.course_name = course_name
        self.field_id = field_id
        self.faculty_id = faculty_id
        self.semester_id = semester_id
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @property
    def serialize(self):
        """
        needed to make Course objects JSON serializable
        """
        return {
            "id": self.id,
            "course_name": self.course_name,
            "field": self.field.serialize,
            "faculty": self.faculty.serialize,
            "semester": self.semester.serialize,
            "grades": [g.serialize for g in self.grades]
        }
    
    def __repr__(self):
        return f"Course({self.course_name}, {self.students})"
