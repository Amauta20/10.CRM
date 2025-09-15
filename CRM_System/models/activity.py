from datetime import datetime

class Activity:
    def __init__(self, type, subject, description=None, related_to=None, related_type=None, due_date=None, completed=False, completed_date=None, assigned_to=None, priority='medium'):
        self.id = None
        self.type = type
        self.subject = subject
        self.description = description
        self.related_to = related_to
        self.related_type = related_type
        self.due_date = due_date
        self.completed = completed
        self.completed_date = completed_date
        self.assigned_to = assigned_to
        self.priority = priority
        self.created_at = datetime.now()