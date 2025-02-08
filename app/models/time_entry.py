from datetime import datetime
from app import db

class TimeEntry(db.Model):
    """Model for storing time tracking entries."""
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    project_code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_invoiced = db.Column(db.Boolean, default=False)
    invoice_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'hours': self.hours,
            'project_code': self.project_code,
            'description': self.description,
            'is_invoiced': self.is_invoiced,
            'invoice_number': self.invoice_number,
            'created_at': self.created_at.isoformat()
        }
