from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.grade import Grade

@app.route("/grades/")
def get_all_grades():
    with db.session_scope() as session:
        all_grades = Grade.get_all(session)
        serialized = [g.serialize for g in all_grades]
        return jsonify(grades=serialized)
