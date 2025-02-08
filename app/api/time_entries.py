from flask import jsonify, request, Blueprint
from flask_login import login_required, current_user
from app.storage.json_storage import JsonTimeEntryStorage
import os

bp = Blueprint('time_entries', __name__)

# Initialize JSON storage
storage = JsonTimeEntryStorage(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                 'data', 'time_entries.json')
)

@bp.route('/api/time-entries', methods=['GET'])
@login_required
def get_time_entries():
    """Get all time entries for the current user."""
    entries = storage.get_user_entries(current_user.id)
    return jsonify(entries)

@bp.route('/api/time-entries', methods=['POST'])
@login_required
def create_time_entry():
    """Create a new time entry."""
    data = request.get_json()
    entry = storage.create_entry(current_user.id, data)
    return jsonify(entry), 201

@bp.route('/api/time-entries/<int:id>', methods=['PUT'])
@login_required
def update_time_entry(id):
    """Update an existing time entry."""
    data = request.get_json()
    entry = storage.update_entry(current_user.id, id, data)
    
    if entry is None:
        return jsonify({'error': 'Entry not found'}), 404
        
    return jsonify(entry)
