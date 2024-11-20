from flask import Flask, send_from_directory
from flask_security import Security
from flask_login import LoginManager
from flask_cors import CORS
import secrets
from flask_sqlalchemy import SQLAlchemy
import os
from flask_restful import Api
from flask_socketio import SocketIO
# Initialize SQLAlchemy
db = SQLAlchemy()
from resources import api
# Import models and resources
from models import *

from datastorefile import datastore
from sample_data import initialize_sample_data

def create_app():
    app = Flask(__name__)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'  # Specify the login view

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Flask configuration   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdb.sqlite3'
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SECURITY_PASSWORD_SALT'] = 'thisnameisnaveen'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['UPLOAD_FOLDER'] = 'uploads/'  # For image uploads
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    CORS(app, resources={
    r"/*": {"origins": "http://localhost:8080", "supports_credentials": True},  # For your API
    r"/login": {"origins": "http://localhost:8080", "supports_credentials": True}   # For the login page
})

    # Initialize components
    db.init_app(app)
    #socketio = SocketIO(app, cors_allowed_origins="*")
    api.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="http://localhost:8080") 
    app.security = Security(app, datastore)

    # Initialize Flask-RESTful API
    
    #api = Api(app)

    # Route to serve Vue.js app
    @app.route('/uploads/<path:filename>')
    def download_file(filename):
        # Remove any directory prefix (e.g., 'uploads/images/') from the filename if present
        filename = filename.replace('uploads/images/', '')  # Strips the prefix if included
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return send_from_directory(app.static_folder, 'index.html')


    return app

# Create Flask app instance
app= create_app()

# Run the Flask app
if __name__ == '__main__':
    initialize_sample_data()

    app.run(debug=True)