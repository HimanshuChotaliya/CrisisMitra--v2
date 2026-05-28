from flask import Blueprint, request, render_template, redirect, url_for, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Sos
from datetime import date
import os

main_bp = Blueprint('main', __name__)

@main_bp.route("/crisismitra")
@jwt_required()
def crisismitra():
    user = get_jwt_identity()
    return render_template("index.html", user=user)

@main_bp.route('/sos', methods=['GET', 'POST'])
@jwt_required()
def sos():
    user_id = get_jwt_identity()
    person = db.session.execute(db.select(User).where(User.id == user_id)).scalar()

    if request.method == 'POST':
        fullname = request.form.get("fullname")
        location = request.form.get("location")
        emergency_type = request.form.get("emergency_type")
        add_detail = request.form.get("add_detail")

        file = request.files.get('evidence')

        # Save inside the app's static assets directory dynamically
        todayis = date.today()
        evidence_path = None
        
        if file and file.filename != "":
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)
            
            # Resolve static folder using Flask current_app context
            full_evidence_path = os.path.join(current_app.static_folder, "assets", "img", filename)
            os.makedirs(os.path.dirname(full_evidence_path), exist_ok=True)
            file.save(full_evidence_path)
            
            # Compatible path format for existing front-end templates
            evidence_path = os.path.join("static/assets/img", filename).replace("\\", "/")

        # Save to database
        report = Sos(
            fullname=fullname,
            location=location,
            emergency_type=emergency_type,
            add_detail=add_detail,
            evidence_path=evidence_path,
            date=todayis            
        )
        
        db.session.add(report)
        person.sos.append(report)
        db.session.commit()

        return render_template('index.html')

    return render_template('sos.html')

@main_bp.route('/redirectmap')
def redirectmap():
    return render_template('map.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
