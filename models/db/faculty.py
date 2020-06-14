from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class Faculty(db.Base):
    """
    model class (maps to faculty table)
    """
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    courses = relationship("Course")

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @property
    def serialize(self):
        """
        needed to make Faculty objects JSON serializable
        """
        return {
            "id": self.id,
            "fname": self.fname,
            "lname": self.lname
        }
    
    def __repr__(self):
        return f"Faculty({self.fname}, {self.lname})"
