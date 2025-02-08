import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class JsonTimeEntryStorage:
    """Handles storage and retrieval of time entries using JSON files."""
    
    def __init__(self, storage_path: str):
        """Initialize the storage with the path to the JSON file."""
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            self._save_entries({})
    
    def _load_entries(self) -> Dict:
        """Load all entries from the JSON file."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_entries(self, entries: Dict):
        """Save entries to the JSON file."""
        with open(self.storage_path, 'w') as f:
            json.dump(entries, f, indent=2)
    
    def get_user_entries(self, user_id: int) -> List[Dict]:
        """Get all time entries for a specific user."""
        entries = self._load_entries()
        user_entries = entries.get(str(user_id), [])
        return sorted(user_entries, key=lambda x: x['created_at'], reverse=True)
    
    def create_entry(self, user_id: int, entry_data: Dict) -> Dict:
        """Create a new time entry for a user."""
        entries = self._load_entries()
        user_id_str = str(user_id)
        
        if user_id_str not in entries:
            entries[user_id_str] = []
            
        user_entries = entries[user_id_str]
        
        new_entry = {
            'id': len(user_entries) + 1,
            'user_id': user_id,
            'hours': float(entry_data['hours']),
            'project_code': entry_data['project_code'],
            'description': entry_data['description'],
            'is_invoiced': entry_data.get('is_invoiced', False),
            'invoice_number': entry_data.get('invoice_number'),
            'created_at': datetime.now().isoformat()
        }
        
        user_entries.append(new_entry)
        self._save_entries(entries)
        return new_entry
    
    def update_entry(self, user_id: int, entry_id: int, entry_data: Dict) -> Optional[Dict]:
        """Update an existing time entry."""
        entries = self._load_entries()
        user_entries = entries.get(str(user_id), [])
        
        for entry in user_entries:
            if entry['id'] == entry_id:
                entry.update({
                    'hours': float(entry_data.get('hours', entry['hours'])),
                    'project_code': entry_data.get('project_code', entry['project_code']),
                    'description': entry_data.get('description', entry['description']),
                    'is_invoiced': entry_data.get('is_invoiced', entry['is_invoiced']),
                    'invoice_number': entry_data.get('invoice_number', entry['invoice_number'])
                })
                self._save_entries(entries)
                return entry
        
        return None
