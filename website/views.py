from flask import Blueprint, flash, jsonify, redirect , render_template,request,url_for 
from flask_login import current_user,login_required 
from website import db
from .models import Note
from datetime import datetime
import json

# Blueprint for the blog section
views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])

@login_required

def home():

    if request.method == 'POST':
        note = request.form['note']
        if note:

            new_note = Note(content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!')
           

    return render_template('home.html',user=current_user)

@views.route('/delete-note', methods=['POST'])

def delete_note():
    note = request.get_json()  # This will give you a dictionary from the incoming JSON data
    note_id = note.get('noteId')  # Extract the noteId from the JSON data
    note = Note.query.get(note_id)  # Fetch the note from the database using the note_id
    
    # Check if the note exists and the current user is authorized to delete it
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({"status": "success"})


