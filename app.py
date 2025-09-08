from flask import Flask, render_template, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
import os
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Use the service account JSON file directly
            cred = credentials.Certificate(Config.get_firebase_credentials_path())
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        return None

# Initialize Firestore client
db = initialize_firebase()

# Import and register blueprints
from api.auth import auth_bp
from api.family import family_bp
from api.sos import sos_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(family_bp, url_prefix='/api')
app.register_blueprint(sos_bp, url_prefix='/api')

@app.route('/')
def home():
    """Serve the home page"""
    return render_template('home.html')

@app.route('/story')
def story():
    """Serve the scrolly-telling story page"""
    return render_template('story.html')

@app.route('/login')
def login():
    """Serve the login/signup page"""
    return render_template('login.html')

@app.route('/app')
def app_page():
    """Serve the main app (original index.html)"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
