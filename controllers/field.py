from flask import render_template, url_for, request, redirect, flash, jsonify
from app import app
from models.dbcontext import DbContext as db
from models.db.field import Field

@app.route("/fields/")
def get_all_fields():
    with db.session_scope() as session:
        all_fields = Field.get_all(session)
        serialized = [f.serialize for f in all_fields]
        return jsonify(fields=serialized)
