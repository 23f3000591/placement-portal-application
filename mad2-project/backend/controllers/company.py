from flask import request, jsonify
from flask_security import auth_token_required, roles_required, current_user
from flask import Blueprint
from controllers.models import *
from controllers.database import db
from datetime import datetime

company = Blueprint("company", __name__)


# =========================
# COMPANY DASHBOARD
# =========================
@company.route("/company/dashboard", methods=["GET"])
@auth_token_required
@roles_required("company")
def company_dashboard():

    company_profile = current_user.company_profile

    total_drives = PlacementDrive.query.filter_by(
        company_id=company_profile.id
    ).count()

    total_applications = Application.query.join(PlacementDrive).filter(
        PlacementDrive.company_id == company_profile.id
    ).count()

    return jsonify({
        "company_name": company_profile.company_name,
        "hr_contact": company_profile.hr_contact,
        "approval_status": company_profile.approval_status,
        "drives": total_drives,
        "applications": total_applications
    }), 200


# =========================
# CREATE DRIVE
# =========================
@company.route("/company/create-drive", methods=["POST"])
@auth_token_required
@roles_required("company")
def create_drive():

    company_profile = current_user.company_profile

    if company_profile.approval_status != "Approved":
        return jsonify({"message": "Company not approved by admin"}), 403

    data = request.json

    deadline_str = data.get("deadline")
    deadline = None
    if deadline_str:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

    drive = PlacementDrive(
        company_id=company_profile.id,
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        min_cgpa=data.get("min_cgpa"),
        allowed_edu_level=data.get("allowed_edu_level"),
        allowed_branch=data.get("allowed_branch"),
        allowed_year=data.get("allowed_year"),
        deadline=deadline
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Placement drive created"}), 201


# =========================
# VIEW COMPANY DRIVES
# =========================
@company.route("/company/drives", methods=["GET"])
@auth_token_required
@roles_required("company")
def view_drives():

    company_profile = current_user.company_profile

    drives = PlacementDrive.query.filter_by(
        company_id=company_profile.id
    ).all()

    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "min_cgpa": drive.min_cgpa,
            "branch": drive.allowed_branch,
            "year": drive.allowed_year,
            "deadline": str(drive.deadline),
            "status": drive.status
        })

    return jsonify(result), 200


# =========================
# VIEW APPLICANTS
# =========================
@company.route("/company/applications/<int:drive_id>", methods=["GET"])
@auth_token_required
@roles_required("company")
def view_applications(drive_id):

    company_profile = current_user.company_profile

    drive = PlacementDrive.query.get(drive_id)

    if not drive or drive.company_id != company_profile.id:
        return jsonify({"message": "Drive not found"}), 404

    applications = Application.query.filter_by(drive_id=drive_id).all()

    result = []

    for app in applications:
        student = app.student

        result.append({
            "application_id": app.id,
            "student_name": student.name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "status": app.status
        })

    return jsonify(result), 200


# =========================
# SHORTLIST STUDENT
# =========================
@company.route("/company/shortlist/<int:application_id>", methods=["POST"])
@auth_token_required
@roles_required("company")
def shortlist_student(application_id):

    application = Application.query.get(application_id)

    if not application or application.drive.company_id != current_user.company_profile.id:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Shortlisted"

    db.session.commit()

    return jsonify({"message": "Student shortlisted"}), 200


# =========================
# SELECT STUDENT
# =========================
@company.route("/company/select/<int:application_id>", methods=["POST"])
@auth_token_required
@roles_required("company")
def select_student(application_id):

    application = Application.query.get(application_id)

    if not application or application.drive.company_id != current_user.company_profile.id:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Selected"

    db.session.commit()

    return jsonify({"message": "Student selected"}), 200


# =========================
# REJECT STUDENT
# =========================
@company.route("/company/reject/<int:application_id>", methods=["POST"])
@auth_token_required
@roles_required("company")
def reject_student(application_id):

    application = Application.query.get(application_id)

    if not application or application.drive.company_id != current_user.company_profile.id:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Rejected"

    db.session.commit()

    return jsonify({"message": "Student rejected"}), 200