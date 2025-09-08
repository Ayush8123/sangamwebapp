from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import firestore
from datetime import datetime
import json

sos_bp = Blueprint('sos', __name__)

@sos_bp.route('/@<user_id>/sos', methods=['POST'])
def trigger_sos(user_id):
    """Trigger SOS alert for user and notify family members"""
    try:
        data = request.get_json() or {}
        
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
        
        # Get user details for the alert
        user_details = {
            'user_id': user_id,
            'username': user_data['username'],
            'email': user_data['email'],
            'mobile_number': user_data['mobile_number']
        }
        
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
                    'mobile_number': member_data['mobile_number']
                })
        
        # Create SOS alert record
        sos_alert = {
            'user_id': user_id,
            'triggered_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'location': data.get('location', 'Unknown'),
            'message': data.get('message', 'Emergency SOS triggered'),
            'family_notified': family_member_ids,
            'user_details': user_details,
            'family_members': family_members
        }
        
        # Store SOS alert in Firestore
        sos_ref = db.collection('sos_alerts').document()
        sos_ref.set(sos_alert)
        
        # Simulate SOS alert notification (in production, this would send actual notifications)
        print("\n" + "="*80)
        print("🚨 SOS ALERT TRIGGERED 🚨")
        print("="*80)
        print(f"User ID: {user_id}")
        print(f"Username: {user_data['username']}")
        print(f"Email: {user_data['email']}")
        print(f"Mobile: {user_data['mobile_number']}")
        print(f"Location: {data.get('location', 'Unknown')}")
        print(f"Message: {data.get('message', 'Emergency SOS triggered')}")
        print(f"Triggered at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("\n📱 FAMILY MEMBERS NOTIFIED:")
        print("-" * 40)
        
        if family_members:
            for i, member in enumerate(family_members, 1):
                print(f"{i}. {member['username']} ({member['user_id']})")
                print(f"   Email: {member['email']}")
                print(f"   Mobile: {member['mobile_number']}")
                print()
        else:
            print("   No family members registered")
            print("   Consider adding family members for emergency contacts")
        
        print("="*80)
        print("🔔 NOTIFICATION SIMULATION:")
        print("   - SMS sent to all family members")
        print("   - Email alerts dispatched")
        print("   - Push notifications sent to mobile apps")
        print("   - Emergency services contacted (if configured)")
        print("="*80 + "\n")
        
        return jsonify({
            'success': True,
            'message': 'SOS alert triggered successfully',
            'alert_id': sos_ref.id,
            'user_id': user_id,
            'triggered_at': sos_alert['triggered_at'],
            'family_members_notified': len(family_members),
            'family_members': family_members,
            'status': 'active'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'SOS alert failed: {str(e)}'
        }), 500

@sos_bp.route('/@<user_id>/sos/history', methods=['GET'])
def get_sos_history(user_id):
    """Get SOS alert history for a user"""
    try:
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
        
        # Get SOS alerts for this user
        sos_alerts_ref = db.collection('sos_alerts')
        sos_alerts = sos_alerts_ref.where('user_id', '==', user_id).order_by('triggered_at', direction=firestore.Query.DESCENDING).get()
        
        alerts = []
        for alert_doc in sos_alerts:
            alert_data = alert_doc.to_dict()
            alerts.append({
                'alert_id': alert_doc.id,
                'triggered_at': alert_data['triggered_at'],
                'status': alert_data['status'],
                'location': alert_data.get('location', 'Unknown'),
                'message': alert_data.get('message', ''),
                'family_members_notified': len(alert_data.get('family_notified', []))
            })
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'alerts': alerts,
            'total_alerts': len(alerts)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get SOS history: {str(e)}'
        }), 500

@sos_bp.route('/@<user_id>/sos/<alert_id>/resolve', methods=['POST'])
def resolve_sos_alert(user_id, alert_id):
    """Resolve an SOS alert"""
    try:
        # Initialize Firestore client
        db = firestore.client()
        
        # Get the SOS alert
        sos_ref = db.collection('sos_alerts').document(alert_id)
        sos_doc = sos_ref.get()
        
        if not sos_doc.exists:
            return jsonify({
                'success': False,
                'error': 'SOS alert not found'
            }), 404
        
        alert_data = sos_doc.to_dict()
        
        # Check if the alert belongs to the user
        if alert_data['user_id'] != user_id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized access to SOS alert'
            }), 403
        
        # Update alert status
        sos_ref.update({
            'status': 'resolved',
            'resolved_at': datetime.utcnow().isoformat()
        })
        
        print(f"\n✅ SOS Alert Resolved: {alert_id}")
        print(f"   User: {user_id}")
        print(f"   Resolved at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        
        return jsonify({
            'success': True,
            'message': 'SOS alert resolved successfully',
            'alert_id': alert_id,
            'resolved_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to resolve SOS alert: {str(e)}'
        }), 500
