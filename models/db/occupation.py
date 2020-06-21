from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

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
    def find_by_id(cls, session, occupation_id: int):
        query = session.query(cls).filter_by(id=occupation_id)
        return query.one()

    @classmethod
    def find_by_name(cls, session, occupation_name: str):
        query = session.query(cls).filter_by(occupation_name=occupation_name)
        return query.one()

    @property
    def serialize(self):
        """
        needed to make Occupation objects JSON serializable
        """
        return {
            "id": self.id,
            "occupation_name": self.occupation_name,
            "median_sal": self.median_sal
        }

    def __repr__(self):
        return f"Occupation({self.id}, {self.occupation_name}, {self.median_sal})"
