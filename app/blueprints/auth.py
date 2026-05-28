from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/user_signin", methods=["GET", "POST"])
def user_signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            print("Access token created")
            resp = jsonify({"msg": "login success"})
            set_access_cookies(resp, access_token)
            return resp, 200

        return jsonify({"msg": "invalid credentials"}), 401

    return render_template("signin.html")

@auth_bp.route("/", methods=["POST","GET"])
def user_signup():
    if request.method == 'POST':
        fullname=request.form.get("yourname")
        contact=request.form.get("contact")
        email=request.form.get("email")
        password=request.form.get("password")
        address=request.form.get("address")
        contact1name=request.form.get("contact1-name")
        contact1phone=request.form.get("contact1-phone")
        contact2name=request.form.get("contact2-name")
        contact2phone=request.form.get("contact2-phone")

        user=db.session.execute(db.select(User).where(User.email==email)).scalar()
        if user:
            return redirect(url_for('auth.user_signin'))

        new_user=User(
            fullname = fullname,
            contact=contact,
            email=email,
            address=address,
            contact1name=contact1name,
            contact1phone=contact1phone,
            contact2name=contact2name,
            contact2phone=contact2phone,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.user_signin'))

    return render_template("register.html")
