import json
from flask import Blueprint, jsonify, render_template, flash, request
from flask_login import login_required, current_user
from .models import Note, User
from . import db

views = Blueprint("views", __name__)

@views.route("/home", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("index.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    node_id = note["note_id"]
    res = Note.query.get(node_id)

    if res:
        if res.user_id == current_user.id:
            db.session.delete(res)
            db.session.commit()
    
    return jsonify({'code': 200})