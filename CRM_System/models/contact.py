from datetime import datetime
from CRM_System.models.base_model import BaseModel

class Contact(BaseModel):
    def __init__(self, first_name, last_name, email=None, phone=None, company=None, company_level=None, job_title=None, referred_by=None):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.company = company
        self.company_level = company_level
        self.job_title = job_title
        self.referred_by = referred_by
        self.status = 'Cliente potencial'  # Cliente potencial, Prospecto, Cliente, Inactivo
        self.assigned_to = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tags = []
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'company_level': self.company_level,
            'job_title': self.job_title,
            'referred_by': self.referred_by,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }