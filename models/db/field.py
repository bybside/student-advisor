from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class Field(db.Base):
    """
    model class (maps to field table)
    """
    __tablename__ = "field"

    id = Column(Integer, primary_key=True)
    field_name = Column(String)
    area = Column(String)
    courses = relationship("Course")

    def __init__(self, field_name, area):
        self.field_name = field_name
        self.area = area
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @property
    def serialize(self):
        """
        needed to make Field objects JSON serializable
        """
        return {
            "id": self.id,
            "field_name": self.field_name,
            "area": self.area
        }

    def __repr__(self):
        return f"Field({self.field_name}, {self.area})"
