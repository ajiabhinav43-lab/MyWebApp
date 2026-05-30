import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from config import DevelopmentConfig
from models import db, User, Doctor, Appointment, Campaign, RecentPatient, ContactMessage
from s3_utils import upload_file_to_s3


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        flash("Admin access required.", "danger")
        return False
    return True


@app.route("/")
def index():
    doctors = Doctor.query.order_by(Doctor.id.desc()).limit(4).all()
    campaigns = Campaign.query.order_by(Campaign.date.asc()).limit(3).all()
    recent_patients = RecentPatient.query.order_by(RecentPatient.visit_date.desc()).limit(5).all()
    return render_template(
        "index.html",
        doctors=doctors,
        campaigns=campaigns,
        recent_patients=recent_patients
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing = User.query.filter_by(email=request.form["email"]).first()
        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=hashed_pw,
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/doctors")
def doctors():
    department = request.args.get("department")
    if department:
        doctors = Doctor.query.filter_by(department=department).all()
    else:
        doctors = Doctor.query.order_by(Doctor.department.asc()).all()

    departments = db.session.query(Doctor.department).distinct().all()
    return render_template("doctors.html", doctors=doctors, departments=departments)


@app.route("/doctor/<int:doctor_id>")
def doctor_detail(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template("doctor_detail.html", doctor=doctor)


@app.route("/appointments")
@login_required
def appointments():
    if current_user.role == "admin":
        appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    else:
        appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.created_at.desc()).all()

    return render_template("appointments.html", appointments=appointments)


@app.route("/appointment/new", methods=["GET", "POST"])
@login_required
def appointment_new():
    doctors = Doctor.query.order_by(Doctor.name.asc()).all()

    if request.method == "POST":
        appointment = Appointment(
            patient_name=request.form["patient_name"],
            patient_age=request.form["patient_age"],
            patient_phone=request.form["patient_phone"],
            patient_problem=request.form["patient_problem"],
            appointment_date=request.form["appointment_date"],
            appointment_time=request.form["appointment_time"],
            doctor_id=request.form["doctor_id"],
            user_id=current_user.id,
            status="Pending"
        )

        db.session.add(appointment)
        db.session.commit()

        flash("Appointment request submitted successfully.", "success")
        return redirect(url_for("appointment_letter", appointment_id=appointment.id))

    return render_template("appointment_form.html", doctors=doctors)


@app.route("/appointment/<int:appointment_id>/letter")
@login_required
def appointment_letter(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if current_user.role != "admin" and appointment.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("appointments"))

    return render_template("appointment_letter.html", appointment=appointment)


@app.route("/appointment/<int:appointment_id>/download")
@login_required
def download_appointment_letter(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if current_user.role != "admin" and appointment.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("appointments"))

    doctor = appointment.doctor

    letter = f"""
CARE YOUR HEALTH HOSPITAL
Appointment Confirmation Letter

Patient Name: {appointment.patient_name}
Age: {appointment.patient_age}
Phone: {appointment.patient_phone}

Doctor: {doctor.name}
Department: {doctor.department}
Qualification: {doctor.qualification}

Appointment Date: {appointment.appointment_date}
Appointment Time: {appointment.appointment_time}
Status: {appointment.status}

Health Concern:
{appointment.patient_problem}

Instructions:
Please arrive 20 minutes before the appointment time.
Carry previous medical records, prescriptions, and ID proof.

Thank you,
Care Your Health Hospital
"""

    return Response(
        letter,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename=appointment_{appointment.id}_letter.txt"}
    )


@app.route("/campaigns")
def campaigns():
    campaigns = Campaign.query.order_by(Campaign.date.asc()).all()
    return render_template("campaigns.html", campaigns=campaigns)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = ContactMessage(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"],
            message=request.form["message"]
        )

        db.session.add(message)
        db.session.commit()

        flash("Your message has been sent successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/admin")
@login_required
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("index"))

    doctor_count = Doctor.query.count()
    appointment_count = Appointment.query.count()
    campaign_count = Campaign.query.count()
    patient_count = RecentPatient.query.count()

    return render_template(
        "admin/dashboard.html",
        doctor_count=doctor_count,
        appointment_count=appointment_count,
        campaign_count=campaign_count,
        patient_count=patient_count
    )


@app.route("/admin/doctor/add", methods=["GET", "POST"])
@login_required
def admin_add_doctor():
    if not admin_required():
        return redirect(url_for("index"))

    if request.method == "POST":
        image_url = request.form.get("image_url")

        file = request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            uploaded_url = upload_file_to_s3(file, filename)
            if uploaded_url:
                image_url = uploaded_url

        doctor = Doctor(
            name=request.form["name"],
            department=request.form["department"],
            qualification=request.form["qualification"],
            experience=request.form["experience"],
            specialization=request.form["specialization"],
            successful_surgeries=request.form["successful_surgeries"],
            achievements=request.form["achievements"],
            image_url=image_url
        )

        db.session.add(doctor)
        db.session.commit()

        flash("Doctor added successfully.", "success")
        return redirect(url_for("doctors"))

    return render_template("admin/add_doctor.html")


@app.route("/admin/campaign/add", methods=["GET", "POST"])
@login_required
def admin_add_campaign():
    if not admin_required():
        return redirect(url_for("index"))

    if request.method == "POST":
        campaign = Campaign(
            title=request.form["title"],
            description=request.form["description"],
            department=request.form["department"],
            date=request.form["date"],
            location=request.form["location"]
        )

        db.session.add(campaign)
        db.session.commit()

        flash("Campaign added successfully.", "success")
        return redirect(url_for("campaigns"))

    return render_template("admin/add_campaign.html")


@app.route("/admin/recent-patients", methods=["GET", "POST"])
@login_required
def admin_recent_patients():
    if not admin_required():
        return redirect(url_for("index"))

    if request.method == "POST":
        patient = RecentPatient(
            patient_name=request.form["patient_name"],
            department=request.form["department"],
            doctor_name=request.form["doctor_name"],
            diagnosis=request.form["diagnosis"],
            status=request.form["status"],
            visit_date=request.form["visit_date"]
        )

        db.session.add(patient)
        db.session.commit()

        flash("Recent patient visit added successfully.", "success")
        return redirect(url_for("admin_recent_patients"))

    patients = RecentPatient.query.order_by(RecentPatient.visit_date.desc()).all()
    return render_template("admin/recent_patients.html", patients=patients)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
