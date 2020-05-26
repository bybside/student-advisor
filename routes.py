from flask import render_template, url_for
from app import app
from models.occupation import Occupation
from models.student import Student
from models.dbcontext import DbContext as db

@app.route("/")
@app.route("/students/")
def get_all_students():
    output = ""
    with db.session_scope() as session:
        all_students = Student.get_all(session)
        return render_template("students.html", students=all_students)

@app.route("/students/<int:student_id>/edit/")
def edit_student(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        return render_template("edit_student.html", student=student)

@app.route("/students/<int:student_id>/delete/")
def delete_student(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        return render_template("delete_student.html", student=student)

# @app.route("/students/create/")
# def create_student():
#     student = Student(fname, lname, dob, grad_year, gpa, occupation)
#     with db.session_scope() as session:
#         Student.add(session, student)

# def create_student(fname: str, lname: str, dob: str, grad_year: int, gpa: float, occupation: Occupation):
#     student = Student(fname, lname, dob, grad_year, gpa, occupation)
#     with db.session_scope() as session:
#         Student.add(session, student)

# def create_occupation(name: str, median_sal: int):
#     occupation = Occupation(name, median_sal)
#     with db.session_scope() as session:
#         Occupation.add(session, occupation)
#     return occupation

# def find_student_by_name(fname: str, lname: str):
#     with db.session_scope() as session:
#         student = Student.find_by_name(session, fname, lname)
#         print(student)
    
# def find_students_by_grad_year(grad_year: int):
#     with db.session_scope() as session:
#         class_of_2013 = Student.find_by_grad_year(session, "2013")
#         print(class_of_2013)

# def get_all_occupations():
#     with db.session_scope() as session:
#         all_occupations = Occupation.get_all(session)
#         for occ in all_occupations:
#             print(occ.students)
