from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import firestore
import string
import random
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def generate_user_id():
    """Generate a unique user ID with prefix and random alphanumeric string"""
    prefix = "SANGAM"
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}_{random_string}"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'mobile_number']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Initialize Firestore client
        db = firestore.client()
        
        # Check if user already exists with this email
        users_ref = db.collection('users')
        existing_user = users_ref.where('email', '==', data['email']).get()
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User with this email already exists'
            }), 409
        
        # Generate unique user ID
        user_id = generate_user_id()
        
        # Prepare user data
        user_data = {
            'user_id': user_id,
            'username': data['username'],
            'email': data['email'],
            'mobile_number': data['mobile_number'],
            'family_members': [],  # Initialize empty family list
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'is_active': True
        }
        
        # Store user in Firestore
        users_ref.document(user_id).set(user_data)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user_id,
            'data': {
                'username': user_data['username'],
                'email': user_data['email'],
                'mobile_number': user_data['mobile_number']
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        
        if 'user_id' not in data or not data['user_id']:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        # Initialize Firestore client
        db = firestore.client()
        
        # Get user data
        user_ref = db.collection('users').document(data['user_id'])
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user_data = user_doc.to_dict()
        
        # Update last login
        user_ref.update({
            'last_login': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user_id': user_data['user_id'],
            'data': {
                'username': user_data['username'],
                'email': user_data['email'],
                'mobile_number': user_data['mobile_number'],
                'family_members': user_data.get('family_members', [])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login failed: {str(e)}'
        }), 500
