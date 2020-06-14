from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.student import Student
from models.snapshot.studentsnapshot import StudentSnapshot

@app.route("/")
@app.route("/students/")
def get_all_students():
    with db.session_scope() as session:
        all_students = Student.get_all(session)
        serialized = [s.serialize for s in all_students]
        return jsonify(students=serialized)

@app.route("/students/<int:student_id>/snapshot/")
def get_snapshot(student_id: int):
    with db.session_scope() as session:
        student = Student.find_by_id(session, student_id)
        class_rank = Student.class_rank(session, student.grad_year, student.id)
        hist_rank = Student.historical_rank(session, student_id)
        # career_fit = Student.career_fit(session, student_id)
        strongest_sub = Student.strongest_sub(session, student_id)
        weakest_sub = Student.weakest_sub(session, student_id)
        snapshot = StudentSnapshot(student=student,
                                   class_rank=class_rank,
                                   hist_rank=hist_rank,
                                   strongest_sub=strongest_sub,
                                   weakest_sub=weakest_sub)
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
