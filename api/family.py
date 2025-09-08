from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import firestore
from datetime import datetime

family_bp = Blueprint('family', __name__)

@family_bp.route('/@<user_id>/add_family', methods=['POST'])
def add_family_member(user_id):
    """Add a family member to user's family list"""
    try:
        data = request.get_json()
        
        if 'family_member_id' not in data or not data['family_member_id']:
            return jsonify({
                'success': False,
                'error': 'Family member ID is required'
            }), 400
        
        family_member_id = data['family_member_id']
        
        # Initialize Firestore client
        db = firestore.client()
        
        # Check if user exists
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Check if family member exists
        family_member_ref = db.collection('users').document(family_member_id)
        family_member_doc = family_member_ref.get()
        
        if not family_member_doc.exists:
            return jsonify({
                'success': False,
                'error': 'Family member not found'
            }), 404
        
        # Get current user data
        user_data = user_doc.to_dict()
        family_members = user_data.get('family_members', [])
        
        # Check if family member is already added
        if family_member_id in family_members:
            return jsonify({
                'success': False,
                'error': 'Family member already added'
            }), 409
        
        # Add family member to the list
        family_members.append(family_member_id)
        
        # Update user document
        user_ref.update({
            'family_members': family_members,
            'updated_at': datetime.utcnow().isoformat()
        })
        
        # Get family member details for response
        family_member_data = family_member_doc.to_dict()
        
        return jsonify({
            'success': True,
            'message': 'Family member added successfully',
            'user_id': user_id,
            'family_member': {
                'user_id': family_member_id,
                'username': family_member_data['username'],
                'email': family_member_data['email'],
                'mobile_number': family_member_data['mobile_number']
            },
            'total_family_members': len(family_members)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to add family member: {str(e)}'
        }), 500

@family_bp.route('/@<user_id>/family', methods=['GET'])
def get_family_members(user_id):
    """Get all family members for a user"""
    try:
        # Initialize Firestore client
        db = firestore.client()
        
        # Get user data
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user_data = user_doc.to_dict()
        family_member_ids = user_data.get('family_members', [])
        
        # Get family member details
        family_members = []
        for member_id in family_member_ids:
            member_ref = db.collection('users').document(member_id)
            member_doc = member_ref.get()
            
            if member_doc.exists:
                member_data = member_doc.to_dict()
                family_members.append({
                    'user_id': member_id,
                    'username': member_data['username'],
                    'email': member_data['email'],
                    'mobile_number': member_data['mobile_number'],
                    'is_active': member_data.get('is_active', True)
                })
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'family_members': family_members,
            'total_count': len(family_members)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get family members: {str(e)}'
        }), 500

@family_bp.route('/@<user_id>/remove_family', methods=['POST'])
def remove_family_member(user_id):
    """Remove a family member from user's family list"""
    try:
        data = request.get_json()
        
        if 'family_member_id' not in data or not data['family_member_id']:
            return jsonify({
                'success': False,
                'error': 'Family member ID is required'
            }), 400
        
        family_member_id = data['family_member_id']
        
        # Initialize Firestore client
        db = firestore.client()
        
        # Get user data
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user_data = user_doc.to_dict()
        family_members = user_data.get('family_members', [])
        
        # Check if family member exists in the list
        if family_member_id not in family_members:
            return jsonify({
                'success': False,
                'error': 'Family member not found in your family list'
            }), 404
        
        # Remove family member from the list
        family_members.remove(family_member_id)
        
        # Update user document
        user_ref.update({
            'family_members': family_members,
            'updated_at': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Family member removed successfully',
            'user_id': user_id,
            'removed_member_id': family_member_id,
            'total_family_members': len(family_members)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to remove family member: {str(e)}'
        }), 500
