from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class Semester(db.Base):
    """
    model class (maps to semester table)
    """
    __tablename__ = "semester"

    id = Column(Integer, primary_key=True)
    semester_name = Column(String)
    academic_year = Column(Integer)
    courses = relationship("Course")

    def __init__(self, semester_name, academic_year):
        self.semester_name
        self.academic_year
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @property
    def serialize(self):
        """
        needed to make Semester objects JSON serializable
        """
        return {
            "id": self.id,
            "semester_name": self.semester_name,
            "academic_year": self.academic_year
        }

    def __repr__(self):
        return f"Semester({self.semester_name}, {self.academic_year})"
