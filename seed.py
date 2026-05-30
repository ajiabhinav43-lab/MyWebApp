from app import app
from models import db, User, Doctor, Campaign, RecentPatient
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    admin = User.query.filter_by(email="admin@careyourhealth.com").first()

    if not admin:
        admin = User(
            username="Admin",
            email="admin@careyourhealth.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin)

    if Doctor.query.count() == 0:
        doctors = [
            Doctor(
                name="Dr. Ananya Menon",
                department="Cardiology",
                qualification="MBBS, MD, DM Cardiology",
                experience="14 Years",
                specialization="Interventional Cardiology, Angioplasty, Heart Failure Care",
                successful_surgeries="820+ cardiac procedures",
                achievements="Led multiple emergency angioplasty success cases and preventive heart-care programs.",
                image_url="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=800&q=80"
            ),
            Doctor(
                name="Dr. Rahul Varma",
                department="Orthopedics",
                qualification="MBBS, MS Orthopedics",
                experience="12 Years",
                specialization="Joint Replacement, Sports Injury, Trauma Care",
                successful_surgeries="650+ orthopedic surgeries",
                achievements="Specialized in knee replacement and fracture reconstruction procedures.",
                image_url="https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=800&q=80"
            ),
            Doctor(
                name="Dr. Meera Nair",
                department="Gynecology",
                qualification="MBBS, MS Obstetrics & Gynecology",
                experience="11 Years",
                specialization="High-risk Pregnancy, Fertility Care, Women Wellness",
                successful_surgeries="500+ safe delivery and gynec procedures",
                achievements="Known for patient-friendly maternal care and successful high-risk pregnancy management.",
                image_url="https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&w=800&q=80"
            ),
            Doctor(
                name="Dr. Arjun Pillai",
                department="Neurology",
                qualification="MBBS, MD, DM Neurology",
                experience="10 Years",
                specialization="Stroke Care, Epilepsy, Neuro Rehabilitation",
                successful_surgeries="300+ neuro-critical recovery cases",
                achievements="Developed rapid stroke-response care pathway for emergency patients.",
                image_url="https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=800&q=80"
            )
        ]

        db.session.add_all(doctors)

    if Campaign.query.count() == 0:
        campaigns = [
            Campaign(
                title="Free Heart Check-up Camp",
                description="Free ECG, blood pressure check, cholesterol screening, and cardiologist consultation.",
                department="Cardiology",
                date="2026-06-10",
                location="Care Your Health Main Campus"
            ),
            Campaign(
                title="Women Wellness Awareness Program",
                description="Free consultation and awareness session for women’s health and pregnancy care.",
                department="Gynecology",
                date="2026-06-18",
                location="Community Health Hall"
            )
        ]

        db.session.add_all(campaigns)

    if RecentPatient.query.count() == 0:
        patients = [
            RecentPatient(
                patient_name="Ramesh K.",
                department="Cardiology",
                doctor_name="Dr. Ananya Menon",
                diagnosis="Post-angioplasty recovery",
                status="Stable",
                visit_date="2026-05-28"
            ),
            RecentPatient(
                patient_name="Lakshmi P.",
                department="Orthopedics",
                doctor_name="Dr. Rahul Varma",
                diagnosis="Knee replacement follow-up",
                status="Recovering well",
                visit_date="2026-05-27"
            )
        ]

        db.session.add_all(patients)

    db.session.commit()

    print("Seed data inserted successfully.")
    print("Admin Login: admin@careyourhealth.com / admin123")
