from models.snapshot.subject import Subject

class StudentSnapshot:
    def __init__(self, student, class_rank, hist_rank, strongest_sub, weakest_sub):
        self.student = student
        self.class_rank = class_rank
        self.hist_rank = hist_rank
        self.strongest_sub = Subject(strongest_sub)
        self.weakest_sub = Subject(weakest_sub)
    
    @property
    def serialize(self):
        """
        needed to make StudentSnapshot objects JSON serializable
        """
        return {
            "student": self.student.serialize,
            "class_rank": self.class_rank,
            "hist_rank": self.hist_rank,
            "strongest_sub": self.strongest_sub.serialize,
            "weakest_sub": self.weakest_sub.serialize
        }
