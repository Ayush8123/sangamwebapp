import os
import json
from firebase_admin import credentials

class Config:
    """Configuration class for the S.A.N.G.A.M. application"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Firebase configuration - using service account JSON file
    FIREBASE_SERVICE_ACCOUNT_PATH = 'firebase_service_account.json'
    
    @classmethod
    def get_firebase_credentials(cls):
        """Get Firebase credentials from JSON file"""
        try:
            with open(cls.FIREBASE_SERVICE_ACCOUNT_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Firebase service account file not found: {cls.FIREBASE_SERVICE_ACCOUNT_PATH}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in Firebase service account file: {cls.FIREBASE_SERVICE_ACCOUNT_PATH}")
    
    @classmethod
    def get_firebase_credentials_path(cls):
        """Get Firebase credentials file path"""
        return cls.FIREBASE_SERVICE_ACCOUNT_PATH
