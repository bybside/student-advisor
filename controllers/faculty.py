from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.faculty import Faculty

@app.route("/faculty/")
def get_all_faculty():
    with db.session_scope() as session:
        all_faculty = Faculty.get_all(session)
        serialized = [f.serialize for f in all_faculty]
        return jsonify(faculty=serialized)
