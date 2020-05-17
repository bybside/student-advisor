from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db
# from models.student import Student

class Occupation(db.Base):
    """
    model class (maps to occupation table)
    """
    __tablename__ = "occupation"

    id = Column(Integer, primary_key=True)
    occupation_name = Column(String)
    median_sal = Column(Integer)
    students = relationship("Student")

    def __init__(self, occupation_name, median_sal):
        self.occupation_name = occupation_name
        self.median_sal = median_sal

    @staticmethod
    def add(session, occupation):
        session.add(occupation)

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_name(cls, session, occupation_name: str):
        query = session.query(cls).filter_by(occupation_name=occupation_name)
        return query.one()

    def __repr__(self):
        return f"Occupation({self.occupation_name}, {self.median_sal})"
