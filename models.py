from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", backref="patient_user", lazy=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(250), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(250), nullable=False)
    successful_surgeries = db.Column(db.String(100), default="0")
    achievements = db.Column(db.Text)
    image_url = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(150), nullable=False)
    patient_age = db.Column(db.String(20), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    patient_problem = db.Column(db.Text, nullable=False)

    appointment_date = db.Column(db.String(50), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Pending")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RecentPatient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    doctor_name = db.Column(db.String(150), nullable=False)
    diagnosis = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
