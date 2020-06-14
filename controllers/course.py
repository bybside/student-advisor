from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.course import Course

@app.route("/courses/")
def get_all_courses():
    with db.session_scope() as session:
        all_courses = Course.get_all(session)
        serialized = [c.serialize for c in all_courses]
        return jsonify(courses=serialized)
