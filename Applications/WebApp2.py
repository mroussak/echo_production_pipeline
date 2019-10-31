# Flask imports:
from flask import Flask, render_template, request, Response, redirect, flash, jsonify, abort, send_file, url_for
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_login import LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.secret_key = 'icardioai'
login_manager = LoginManager()
login_manager.init_app(app)
    
# Script imports:
from .UsersApp.Components import Models
from .UsersApp.Components.Functions import ValidateUser, RegisterUser
from .UsersApp.Components.Models import User
# import ProductionWebApp.Components.FileHandler as files
# import ProductionWebApp.Components.Security as security
# import UserLoginApp.Components.Sessions as sessions
from time import time, sleep
from pprint import pprint
import subprocess
import json
import sys
import os

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline/')
from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = 'sqlite://webapp.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'philippe@icardio.ai'
    MAIL_PASSWORD = 'yRVT*6VB'
    MAIL_DEFAULT_SENDER = '"iCardio.ai Team" <philippe@icardio.ai>'

    # Flask-User settings
    USER_APP_NAME = "iCardio.ai User Management"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "philippe@icardio.ai"

app.config.from_object(__name__+'.ConfigClass')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

user_manager = UserManager(app, db, User)


# Front page:
@app.route('/')
def front_page():
    return render_template('index.html')


# Log in page:
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    
    if request.method == 'POST':
        
        # read email, password from front end:
        email = request.form.get('email')
        password = request.form.get('password')
        
        # validate user:
        validation = ValidateUser(email, user_manager.hash_password(password), verbose=True)

        # redirect if credentials are incorrect:
        if validation['code'] == -1 or validation['code'] == 0 or validation['code'] == 1:
            flash(validation['message'])
            return render_template('login.html')
        
        # log user in if credentials are correct:
        else:
            user = tmvalidation['result']
            login_user(user)
            return render_template('apps.html')
        
    return render_template('login.html')
    

# Register page:    
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    
    if request.method == 'POST':
        
        # read email, password, name, tel from front end:
        email = request.form.get('email')
        password = request.form.get('pass')
        name = request.form.get('name')
        tel = request.form.get('tel')
        
        # validate user:
        validation = RegisterUser(email, user_manager.hash_password(password), name, tel, verbose=True)
        print(validation)

        # redirect if credentials are incorrect:
        if validation['code'] == 0 or validation['code'] == 1:
            flash(validation['message'])
            return render_template('register.html')
        
        # register and login user in if credentials are correct:
        else:
            user = validation['result']
            login_user(user)
            return render_template('apps.html')
            
    return render_template('register.html')
    

# Apps page:
@app.route('/apps')
@login_required
def apps_page():
    return render_template('apps.html')
    

# Upload dicom page:
@app.route('/upload')
@login_required
def upload_dicom_page():
    return render_template('upload.html')
    

# Views validation page:
@app.route('/validator')
@login_required
def views_validation_page():
    return render_template('validator.html')
    
    

   
# Main: 

# Variables:
verbose = True
start = time()   
file_paths = {
    'status_file' : '/internal_drive/echo_production_pipeline/Flask/static/status.txt',
}
# Load models:
#ModelsPipeline.main(start=time())

# Dev functions:
if __name__ == "__main__":
    # Intialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    # Launch app:
    app.run(debug=True, use_reloader=False)
    manager.run()
