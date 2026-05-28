from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Volunteer, Sos, Skill, User
from datetime import date
import requests

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/volunteer_login', methods=["GET", "POST"])
def volunteer_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        # Intercept admin login credentials
        if email == "admin@gmail.com" and password == "@dmin":
            session['is_admin'] = True
            return redirect(url_for('volunteer.volunteer'))
            
        result = db.session.execute(db.select(Volunteer).where(Volunteer.email == email)).scalar()
        if result and result.password == password:
            session['is_admin'] = False
            return redirect(url_for('volunteer.volunteer'))          
    return render_template('login.html')

@volunteer_bp.route('/volunteer_signup', methods=["POST", "GET"])
@jwt_required()
def volunteer_signup():
    user_id = get_jwt_identity()
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        loc = request.form.get('loc')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        todayis = date.today()
        
        person = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
        user = db.session.execute(db.select(Volunteer).where(Volunteer.email == email)).scalar()
        
        if password != cpassword:
            return redirect(url_for('volunteer.volunteer_signup'))
        
        elif user is not None:
            return redirect(url_for('volunteer.volunteer_login'))

        else:
            newv = Volunteer(
                fname=fname,
                lname=lname,
                email=email,
                loc=loc,
                date=todayis
            )
            newv.set_password(password)
            db.session.add(newv)
            person.volunteers.append(newv)
            db.session.commit()

            return redirect(url_for('volunteer.volunteer'))
        
    return render_template('signup.html')

@volunteer_bp.route('/volunteer')
def volunteer():
    vol_info = db.session.execute(db.select(Volunteer).order_by(Volunteer.loc)).scalars().all()
    sos_info = db.session.execute(db.select(Sos).order_by(Sos.id)).scalars().all()
    area_name = None
    
    for y in sos_info:
        coords = y.location
        try:
            lat, lon = [float(x.strip()) for x in coords.split(",")]
            url = "https://nominatim.openstreetmap.org/reverse"
            parameters = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "zoom": 18,
                "addressdetails": 1
            }
            headers = {
                "User-Agent": "CrisisMitra/1.0 (contact: himanshu746h@gmail.com)"
            }

            response = requests.get(url, params=parameters, headers=headers, timeout=10)
            data = response.json()
            area_name = data['address'].get('suburb', data['address'].get('neighbourhood', 'Unknown'))
        except Exception as e:
            print(f"Error resolving geocode for {coords}: {e}")
            area_name = "Unknown Location"
            
    return render_template('volunteer.html', vol_info=vol_info, sos_info=sos_info, area=area_name)

@volunteer_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('volunteer.volunteer_login'))

@volunteer_bp.route('/dismiss_sos/<int:sos_id>')
def dismiss_sos(sos_id):
    # Only allow authenticated admin to dismiss SOS signals
    if not session.get('is_admin'):
        abort(403)
        
    sos_entry = db.session.execute(db.select(Sos).where(Sos.id == sos_id)).scalar()
    if sos_entry:
        db.session.delete(sos_entry)
        db.session.commit()
        
    return redirect(url_for('volunteer.volunteer'))

@volunteer_bp.route('/evaluate/<int:volid>', methods=["GET", "POST"])
def certify(volid):
    # Restrict skills certification to admin users only
    if not session.get('is_admin'):
        abort(403)

    if request.method == 'POST':
        responses = [
            request.form.get('first_aid'),
            request.form.get('search'),
            request.form.get('cpr_certified'),
            request.form.get('emtb')
        ]

        listed_skills = [
            'First Aid',
            'Search & Rescue',
            'CPR Certified',
            'EMT-B'
        ]
        
        person = db.session.execute(db.select(Volunteer).where(Volunteer.id == volid)).scalar()

        for response, skill_name in zip(responses, listed_skills):
            if response == "yes":
                skill = Skill.query.filter_by(skill_name=skill_name).first()
                if skill not in person.skills:
                    person.skills.append(skill)

            if response == "no":
                skill = Skill.query.filter_by(skill_name=skill_name).first()
                if skill in person.skills:
                    person.skills.remove(skill)
                        
        db.session.commit()
        return redirect(url_for('volunteer.volunteer'))

    return render_template('certify.html', volid=volid)
