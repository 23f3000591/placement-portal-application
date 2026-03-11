from flask import request, jsonify
from flask_security import auth_token_required, roles_required, current_user
from flask import Blueprint
from controllers.models import *
from controllers.database import db
from datetime import date

student = Blueprint("student", __name__)

@student.route("/export-csv", methods=["GET"])
def export_csv():

    from celery_app import generate_csv 

    generate_csv.delay()

    return {"message": "CSV export started"}


# =========================
# STUDENT DASHBOARD
# =========================
@student.route("/student/dashboard", methods=["GET"])
@auth_token_required
@roles_required("student")
def student_dashboard():

    student_profile = current_user.student_profile

    total_applications = Application.query.filter_by(
        student_id=student_profile.id
    ).count()

    selected = Application.query.filter_by(
        student_id=student_profile.id,
        status="Selected"
    ).count()

    return jsonify({
        "name": student_profile.name,
        "branch": student_profile.branch,
        "year": student_profile.year,
        "cgpa": student_profile.cgpa,
        "applications": total_applications,
        "selected": selected
    }), 200


# =========================
# VIEW ELIGIBLE DRIVES
# =========================
@student.route("/student/drives", methods=["GET"])
@auth_token_required
@roles_required("student")
def view_drives():

    student_profile = current_user.student_profile

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    result = []

    for drive in drives:

        if drive.deadline < date.today():
            continue

        if student_profile.cgpa < drive.min_cgpa:
            continue

        if student_profile.edu_level != drive.allowed_edu_level:
            continue

        branches = [b.strip() for b in drive.allowed_branch.split(",")]

        if student_profile.branch not in branches:
            continue

        if student_profile.year != drive.allowed_year:
            continue
        
        existing = Application.query.filter_by(
            student_id=student_profile.id,
            drive_id=drive.id
        ).first()
        
        result.append({
            "id": drive.id,
            "company": drive.company.company_name,
            "job_title": drive.job_title,
            "description": drive.job_description,
            "min_cgpa": drive.min_cgpa,
            "branch": drive.allowed_branch,
            "year": drive.allowed_year,
            "deadline": str(drive.deadline),
            "applied": True if existing else False
        })

    return jsonify(result), 200


# =========================
# APPLY TO DRIVE
# =========================
@student.route("/student/apply/<int:drive_id>", methods=["POST"])
@auth_token_required
@roles_required("student")
def apply_drive(drive_id):

    student_profile = current_user.student_profile

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status != "Approved":
        return jsonify({"message": "Drive not open"}), 400

    if drive.deadline < date.today():
        return jsonify({"message": "Application deadline passed"}), 400

    if student_profile.cgpa < drive.min_cgpa:
        return jsonify({"message": "CGPA criteria not met"}), 400

    if student_profile.edu_level != drive.allowed_edu_level:
        return jsonify({"message": "Education level not eligible"}), 400

    branches = [b.strip() for b in drive.allowed_branch.split(",")]

    if student_profile.branch not in branches:
        return jsonify({"message": "Branch not eligible"}), 400

    if student_profile.year != drive.allowed_year:
        return jsonify({"message": "Year not eligible"}), 400

    existing = Application.query.filter_by(
        student_id=student_profile.id,
        drive_id=drive.id
    ).first()

    if existing:
        return jsonify({"message": "Already applied"}), 400

    application = Application(
        student_id=student_profile.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted"}), 201


# =========================
# VIEW APPLICATIONS
# =========================
@student.route("/student/applications", methods=["GET"])
@auth_token_required
@roles_required("student")
def view_applications():

    student_profile = current_user.student_profile

    applications = Application.query.filter_by(
        student_id=student_profile.id
    ).all()

    result = []

    for app in applications:
        result.append({
            "application_id": app.id,
            "company": app.drive.company.company_name,
            "job_title": app.drive.job_title,
            "status": app.status,
            "applied_on": str(app.application_date)
        })

    return jsonify(result), 200


# =========================
# UPDATE PROFILE
# =========================
@student.route("/student/profile", methods=["PUT"])
@auth_token_required
@roles_required("student")
def update_profile():

    student_profile = current_user.student_profile

    data = request.json

    student_profile.github = data.get("github", student_profile.github)
    student_profile.linkedin = data.get("linkedin", student_profile.linkedin)
    student_profile.contact = data.get("contact", student_profile.contact)
    student_profile.cgpa = data.get("cgpa", student_profile.cgpa)

    db.session.commit()

    return jsonify({"message": "Profile updated"}), 200