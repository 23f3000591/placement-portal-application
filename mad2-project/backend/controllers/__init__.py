from flask import Flask
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from controllers.models import User, Role
from controllers.database import db
from controllers.auth import auth
from controllers.admin import admin
from controllers.student import student
from controllers.company import company
from controllers.user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'Harshad@placement_portal_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'Harshad_placement_portal_salt'
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(student, url_prefix='/')
    app.register_blueprint(company, url_prefix='/')
    
    db.init_app(app)
    
    security = Security(app, user_datastore)
    
    with app.app_context():
        db.create_all()
        
        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        company_role = user_datastore.find_or_create_role(name='company', description='Company User')
        student_role = user_datastore.find_or_create_role(name='student', description='Student User')
        
        if not user_datastore.find_user(email='admin@gmail.com'):
            admin_user = user_datastore.create_user(
                email = "admin@gmail.com",
                roles = [admin_role]
            )
            admin_user.set_password("Admin@123")
        db.session.commit()
    
    return app