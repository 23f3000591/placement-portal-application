from flask import request, jsonify
from flask_security import utils, auth_token_required, roles_required
from flask import Blueprint
from controllers.models import *
from controllers.user_datastore import user_datastore
from controllers.database import db

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard", methods=["GET"])
@auth_token_required
@roles_required("admin")
def admin_dashboard():

    total_students = StudentProfile.query.count()
    total_companies = CompanyProfile.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    }), 200
    
# View All Companies
@admin.route("/admin/companies", methods=["GET"])
@auth_token_required
@roles_required("admin")
def get_companies():

    companies = CompanyProfile.query.all()

    result = []

    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "hr_contact": company.hr_contact,
            "approval_status": company.approval_status,
            "email": company.user.email,
            "is_blacklisted": company.user.is_blacklisted,
            "user_id": company.user.id
        })

    return jsonify(result), 200

# Approve Company
@admin.route("/admin/company/approve/<int:company_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def approve_company(company_id):

    company = CompanyProfile.query.get(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.approval_status = "Approved"

    db.session.commit()

    return jsonify({"message": "Company approved successfully"}), 200

# Reject Company
@admin.route("/admin/company/reject/<int:company_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def reject_company(company_id):

    company = CompanyProfile.query.get(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.approval_status = "Rejected"

    db.session.commit()

    return jsonify({"message": "Company rejected"}), 200

# View Students
@admin.route("/admin/students", methods=["GET"])
@auth_token_required
@roles_required("admin")
def get_students():

    students = StudentProfile.query.all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "user_id": student.user.id,
            "name": student.name,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa,
            "email": student.user.email,
            "is_blacklisted": student.user.is_blacklisted
        })

    return jsonify(result), 200

# Blacklist User
@admin.route("/admin/blacklist/<int:user_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def blacklist_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_blacklisted = True
    user.active = False

    db.session.commit()

    return jsonify({"message": "User blacklisted"}), 200

# Unblacklist User
@admin.route("/admin/unblacklist/<int:user_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def unblacklist_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_blacklisted = False
    user.active = True

    db.session.commit()

    return jsonify({"message": "User unblacklisted successfully"}), 200

# View Placement Drives
@admin.route("/admin/drives", methods=["GET"])
@auth_token_required
@roles_required("admin")
def get_drives():

    drives = PlacementDrive.query.all()

    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "company": drive.company.company_name,
            "job_title": drive.job_title,
            "min_cgpa": drive.min_cgpa,
            "allowed_branch": drive.allowed_branch,
            "deadline": str(drive.deadline),
            "status": drive.status
        })

    return jsonify(result), 200

# Approve Placement Drive
@admin.route("/admin/drive/approve/<int:drive_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def approve_drive(drive_id):

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Approved"

    db.session.commit()

    return jsonify({"message": "Drive approved"}), 200

# Reject Placement Drive
@admin.route("/admin/drive/reject/<int:drive_id>", methods=["POST"])
@auth_token_required
@roles_required("admin")
def reject_drive(drive_id):

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Rejected"

    db.session.commit()

    return jsonify({"message": "Drive rejected"}), 200