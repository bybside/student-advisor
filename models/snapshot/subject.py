class Subject:
    def __init__(self, subject_data: tuple):
        self.field_name = subject_data[0]
        self.area = subject_data[1]
        self.avg_grade = round(subject_data[2], 2)
    
    @property
    def serialize(self):
        """
        needed to make Subject objects JSON serializable
        """
        return {
            "field_name": self.field_name,
            "area": self.area,
            "avg_grade": float(self.avg_grade)
        }
