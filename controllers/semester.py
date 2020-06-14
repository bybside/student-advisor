from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.semester import Semester

@app.route("/semesters/")
def get_all_semesters():
    with db.session_scope() as session:
        all_semesters = Semester.get_all(session)
        serialized = [s.serialize for s in all_semesters]
        return jsonify(semesters=serialized)
