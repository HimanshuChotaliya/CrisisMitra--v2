from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Mapped , mapped_column, relationship


volunteers_skill = db.Table(
    'volunteers_skill',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


user_sos = db.Table(
    'user_sos',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('sos_id', db.Integer, db.ForeignKey('sos_entries.id'), primary_key=True)
)

user_volunteer = db.Table(
    'user_volunteer',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True)
)

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    fullname =db.Column(db.String, nullable=False)
    contact=db.Column(db.String, nullable=False,unique=True)
    email = db.Column(db.String, nullable=False,unique=True)
    address= db.Column(db.String, nullable=True)
    contact1name=db.Column(db.String, nullable=True)
    contact1phone=db.Column(db.String, nullable=True)
    contact2name=db.Column(db.String, nullable=True)
    contact2phone=db.Column(db.String, nullable=True)
    password =db.Column(db.String, nullable=False)
    #sos = db.relationship('Sos', backref='user', lazy='dynamic')
    #volunteer = db.relationship('Volunteer', backref='user', lazy='dynamic')
    
    volunteers: Mapped[list["Volunteer"]] = db.relationship(
        secondary=user_volunteer,
        back_populates="users"
    )

    sos: Mapped[list["Sos"]] = db.relationship(
        secondary=user_sos,
        back_populates="users"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    



class Sos(db.Model):
    __tablename__="sos_entries"
    id= db.Column(db.Integer, primary_key=True)
    fullname=db.Column(db.String, nullable=False)
    location=db.Column(db.String, nullable=False)
    emergency_type=db.Column(db.String, nullable=False)
    add_detail=db.Column(db.String, nullable=True)
    evidence_path =db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=False)
    #user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users: Mapped[list["User"]] = db.relationship(
        secondary=user_sos,
        back_populates="sos"
    )

class Volunteer( db.Model):
    __tablename__ = 'volunteers'

    id= db.Column(db.Integer,primary_key=True)
    fname= db.Column(db.String, nullable=False)
    lname= db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False)
    loc = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    password= db.Column(db.String, nullable=False)
    #user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #skill = db.relationship('Skill', backref='volunteer', lazy='dynamic')
    skills: Mapped[list["Skill"]] = db.relationship(
        secondary=volunteers_skill,
        back_populates="volunteers"
    )

    users: Mapped[list["User"]] = db.relationship(
        secondary=user_volunteer,
        back_populates="volunteers"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)    
    
class Skill(db.Model):
    __tablename__ = 'skill'

    id=db.Column(db.Integer,primary_key=True)
    skill_name= db.Column(db.String, unique=True, nullable=False) 
    #volunteer_id=db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    volunteers: Mapped[list["Volunteer"]] = db.relationship(
        secondary=volunteers_skill,
        back_populates="skills"
    )
