from collections import defaultdict
from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.student import Student
from models.db.occupation import Occupation
from models.db.studentsnapshot import StudentSnapshot

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
        snapshot = StudentSnapshot.find_by_id(session, student_id)
        return jsonify(snapshot=snapshot.serialize)

@app.route("/students/<int:student_id>/career-fit/")
def get_career_fit(student_id: int):
    with db.session_scope() as session:
        serialized = defaultdict(dict)
        top_students, top_occupations = Student.career_fit(session, student_id)
        for sid, score in top_students:
            student = Student.find_by_id(session, sid)
            serialized["top_students"][sid] = {
                "fname": student.fname,
                "lname": student.lname,
                "occupation": student.occupation.serialize,
                "score": score
            }
        for oid, score in top_occupations:
            occupation = Occupation.find_by_id(session, oid)
            serialized["top_occupations"][oid] = {
                "occupation": occupation.serialize,
                "score": score
            }
        return jsonify(career_fit=serialized)

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
