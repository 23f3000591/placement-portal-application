from flask import request, jsonify
from flask_security import utils, auth_token_required
from flask import Blueprint
from controllers.models import User, Role, CompanyProfile, StudentProfile
from controllers.user_datastore import user_datastore
from controllers.database import db

auth = Blueprint("auth", __name__)


# =========================
# STUDENT REGISTER API
# =========================
@auth.route('/student/register', methods=['POST'])
def register_student():
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    edu_level = request.json.get("edu_level")
    branch = request.json.get("branch")
    year = request.json.get("year")
    contact = request.json.get("contact")
    cgpa = request.json.get("cgpa")
    github = request.json.get("github")
    linkedin = request.json.get("linkedin")

    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not email.endswith('@gmail.com'):
        return jsonify({"message": "Email must be a valid Gmail address"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if not edu_level:
        return jsonify({"message": "Education level is required"}), 400
    if not branch:
        return jsonify({"message": "Branch is required"}), 400
    if not year:
        return jsonify({"message": "Year is required"}), 400
    if not contact:
        return jsonify({"message": "Contact is required"}), 400
    if not cgpa:
        return jsonify({"message": "CGPA is required"}), 400

    if user_datastore.find_user(email=email):
        return jsonify({"message": "Email already registered"}), 400

    student_role = user_datastore.find_role('student')

    user = user_datastore.create_user(
        email=email,
        roles=[student_role]
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    student_profile = StudentProfile(
        user_id=user.id,
        name=name,
        edu_level=edu_level,
        branch=branch,
        year=year,
        contact=contact,
        cgpa=cgpa,
        github=github,
        linkedin=linkedin,
    )

    db.session.add(student_profile)
    db.session.commit()

    return jsonify({
        "message": "Student registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "roles": [role.name for role in user.roles]
        },
        "student_profile": {
            "name": student_profile.name,
            "branch": student_profile.branch,
            "year": student_profile.year,
            "contact": student_profile.contact,
            "cgpa": student_profile.cgpa,
            "github": student_profile.github,
            "linkedin": student_profile.linkedin
        }
    }), 201


# =========================
# COMPANY REGISTER API
# =========================
@auth.route('/company/register', methods=['POST'])
def register_company():
    email = request.json.get("email")
    password = request.json.get("password")
    company_name = request.json.get("company_name")
    hr_contact = request.json.get("hr_contact")

    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not email.endswith('@gmail.com'):
        return jsonify({"message": "Email must be a valid Gmail address"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400
    if not company_name:
        return jsonify({"message": "Company name is required"}), 400
    if not hr_contact:
        return jsonify({"message": "HR contact is required"}), 400

    if user_datastore.find_user(email=email):
        return jsonify({"message": "Email already registered"}), 400

    company_role = user_datastore.find_role('company')

    user = user_datastore.create_user(
        email=email,
        roles=[company_role]
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    company_profile = CompanyProfile(
        user_id=user.id,
        company_name=company_name,
        hr_contact=hr_contact
    )

    db.session.add(company_profile)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "roles": [role.name for role in user.roles]
        }
    }), 201


# =========================
# LOGIN API
# =========================
@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400

    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "Invalid email"}), 401

    if not user.check_password(password):
        return jsonify({"message": "Invalid password"}), 401

    # NEW CHECK
    if user.is_blacklisted:
        return jsonify({"message": "Your account has been blacklisted by admin"}), 403

    if not user.active:
        return jsonify({"message": "Your account is inactive"}), 403

    auth_token = user.get_auth_token()
    utils.login_user(user)

    return jsonify({
        "message": "Login successful",
        "auth_token": auth_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "roles": [role.name for role in user.roles]
        }
    }), 200


# =========================
# LOGOUT API
# =========================
@auth.route('/logout', methods=['POST'])
@auth_token_required
def logout():
    utils.logout_user()
    return jsonify({"message": "Logout successful"}), 200