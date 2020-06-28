from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.dbcontext import DbContext as db

class StudentSnapshot(db.Base):
    """
    model class (maps to snapshot table)
    """
    __tablename__ = "student_snapshot"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    student = relationship("Student", uselist=False)
    class_rank = Column(Integer)
    hist_rank = Column(Integer)
    strongest_sub_id = Column(Integer, ForeignKey("field.id"))
    strongest_sub = relationship("Field", foreign_keys=[strongest_sub_id])
    strongest_sub_avg = Column(Float)
    weakest_sub_id = Column(Integer, ForeignKey("field.id"))
    weakest_sub = relationship("Field", foreign_keys=[weakest_sub_id])
    weakest_sub_avg = Column(Float)

    def __init__(self, student_id, class_rank, hist_rank, strongest_sub, weakest_sub):
        self.student_id = student_id
        self.class_rank = class_rank
        self.hist_rank = hist_rank
        self.strongest_sub_id, self.strongest_sub_avg = strongest_sub
        self.weakest_sub_id, self.weakest_sub_avg = weakest_sub

    @classmethod
    def find_by_id(cls, session, student_id: int):
        query = session.query(cls).filter_by(student_id=student_id)
        return query.one()

    @property
    def serialize(self):
        """
        needed to make StudentSnapshot objects JSON serializable
        """
        return {
            "student": self.student.serialize,
            "class_rank": self.class_rank,
            "hist_rank": self.hist_rank,
            "strongest_sub": {
                "field": self.strongest_sub.serialize,
                "avg": self.strongest_sub_avg
            },
            "weakest_sub": {
                "field": self.weakest_sub.serialize,
                "avg": self.weakest_sub_avg
            }
        }
