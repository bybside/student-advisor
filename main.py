from models.occupation import Occupation
from models.student import Student
from models.dbcontext import DbContext as db

def main():
    occupation = create_occupation("Programmer Analyst", 75000)
    create_student("Johnny", "Football", "09-19-1995", 2013, 3.85, occupation)
    find_student_by_name("Johnny", "Football")
    find_students_by_grad_year(2013)
    get_all_students()
    get_all_occupations()

def create_occupation(name: str, median_sal: int):
    occupation = Occupation(name, median_sal)
    with db.session_scope() as session:
        Occupation.add(session, occupation)
    return occupation

def create_student(fname: str, lname: str, dob: str, grad_year: int, gpa: float, occupation: Occupation):
    student = Student(fname, lname, dob, grad_year, gpa, occupation)
    with db.session_scope() as session:
        Student.add(session, student)

def find_student_by_name(fname: str, lname: str):
    with db.session_scope() as session:
        student = Student.find_by_name(session, fname, lname)
        print(student)
    
def find_students_by_grad_year(grad_year: int):
    with db.session_scope() as session:
        class_of_2013 = Student.find_by_grad_year(session, "2013")
        print(class_of_2013)

def get_all_students():
    with db.session_scope() as session:
        all_students = Student.get_all(session)
        for student in all_students:
            print(student.occupation)

def get_all_occupations():
    with db.session_scope() as session:
        all_occupations = Occupation.get_all(session)
        for occ in all_occupations:
            print(occ.students)
    
main()
