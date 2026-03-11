from controllers.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    is_blacklisted = db.Column(db.Boolean(), default=False)
    
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    
    roles = db.relationship('Role', secondary='user_roles')
    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    
# Company Table
class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    approval_status = db.Column(db.String(20), default='Pending')  # Pending / Approved / Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))

# Student Table
class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    edu_level = db.Column(db.String(200), nullable=False) # Bachelors / Masters
    branch = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float)
    contact = db.Column(db.String(15))
    github = db.Column(db.String(200)) # github profile link
    linkedin = db.Column(db.String(200)) # linkedin profile link
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

# Placement Drive Table
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    allowed_edu_level = db.Column(db.String(200), nullable=False) # Bachelors / Masters
    allowed_branch = db.Column(db.String(100), nullable=False)
    allowed_year = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending / Approved / Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('CompanyProfile', backref='drives')

# Application Table
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Applied') # Applied / Shortlisted / Selected / Rejected
    
    student = db.relationship('StudentProfile', backref='applications')
    drive = db.relationship('PlacementDrive', backref='applications')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )