from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db
# from models.occupation import Occupation

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

    def __init__(self, fname, lname, dob, grad_year, gpa, occupation):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.grad_year = grad_year
        self.gpa = gpa
        self.occupation = occupation
    
    @staticmethod
    def add(session, student):
        session.add(student)
    
    @staticmethod
    def delete(session, student):
        session.delete(student)
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, student_id: int):
        query = session.query(cls).filter_by(id=student_id)
        return query.one()

    @classmethod
    def find_by_name(cls, session, fname: str, lname: str):
        query = session.query(cls).filter_by(lname=lname, fname=fname)
        return query.one()
    
    @classmethod
    def find_by_grad_year(cls, session, grad_year: int):
        query = session.query(cls).filter_by(grad_year=grad_year)
        return query.all()
    
    # @classmethod
    # def find_by_gpa(cls, gpa: float):
    #     session = db.Session()
    #     query = session.query(cls).filter_by(gpa=gpa)
    #     return query.all()

    @property
    def serialize(self):
        """
        needed to make Student objects JSON serializable
        """
        return {
            "fname": self.fname,
            "lname": self.lname,
            "dob": self.dob,
            "grad_year": self.grad_year,
            "gpa": self.gpa,
            "occupation": self.occupation.occupation_name
        }
    
    def __repr__(self):
        return f"Student({self.fname}, {self.lname}, {self.dob}, {self.grad_year}, {self.gpa})"
