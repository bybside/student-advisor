from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.occupation import Occupation
from models.student import Student
from models.course import Course
from models.faculty import Faculty
from models.field import Field
from models.semester import Semester
from models.grade import Grade
from models.dbcontext import DbContext as db

@app.route("/")
@app.route("/students/")
def get_all_students():
    with db.session_scope() as session:
        all_students = Student.get_all(session)
        serialized = [s.serialize for s in all_students]
        return jsonify(students=serialized)

@app.route("/courses/")
def get_all_courses():
    with db.session_scope() as session:
        all_courses = Course.get_all(session)
        serialized = [c.serialize for c in all_courses]
        return jsonify(courses=serialized)

@app.route("/occupations/")
def get_all_occupations():
    with db.session_scope() as session:
        all_occupations = Occupation.get_all(session)
        serialized = [o.serialize for o in all_occupations]
        return jsonify(occupations=serialized)

@app.route("/faculty/")
def get_all_faculty():
    with db.session_scope() as session:
        all_faculty = Faculty.get_all(session)
        serialized = [f.serialize for f in all_faculty]
        return jsonify(faculty=serialized)

@app.route("/fields/")
def get_all_fields():
    with db.session_scope() as session:
        all_fields = Field.get_all(session)
        serialized = [f.serialize for f in all_fields]
        return jsonify(fields=serialized)

@app.route("/semesters/")
def get_all_semesters():
    with db.session_scope() as session:
        all_semesters = Semester.get_all(session)
        serialized = [s.serialize for s in all_semesters]
        return jsonify(semesters=serialized)

@app.route("/grades/")
def get_all_grades():
    with db.session_scope() as session:
        all_grades = Grade.get_all(session)
        serialized = [g.serialize for g in all_grades]
        return jsonify(grades=serialized)

@app.route("/students/<int:student_id>/snapshot/")
def get_snapshot(student_id: int):
    with db.session_scope() as session:
        snapshot = Student.snapshot(session, student_id)
        return jsonify(snapshot=snapshot.serialize)

@app.route("/students/<int:student_id>/")
def get_student(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        return jsonify(student=student.serialize)

@app.route("/students/<int:student_id>/edit/", methods=["POST"])
def edit_student(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        student.fname = request.form["fname"]
        student.lname = request.form["lname"]
        student.dob = request.form["dob"]
        student.grad_year = request.form["grad_year"]
        student.gpa = request.form["gpa"]
        Student.add(session, student)

@app.route("/students/<int:student_id>/delete/", methods=["POST"])
def delete_student(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        Student.delete(session, student)

@app.route("/students/create/", methods=["POST"])
def create_student():
    with db.session_scope() as session:
        occupation = Occupation.find_by_name(session, request.form["occupation_name"])
        student = Student(fname=request.form["fname"],
                          lname=request.form["lname"],
                          dob=request.form["dob"],
                          grad_year=request.form["grad_year"],
                          gpa=request.form["gpa"],
                          occupation=occupation)
        Student.add(session, student)

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
