from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.occupation import Occupation

@app.route("/occupations/")
def get_all_occupations():
    with db.session_scope() as session:
        all_occupations = Occupation.get_all(session)
        serialized = [o.serialize for o in all_occupations]
        return jsonify(occupations=serialized)

# def create_occupation(name: str, median_sal: int):
#     occupation = Occupation(name, median_sal)
#     with db.session_scope() as session:
#         Occupation.add(session, occupation)
#     return occupation
