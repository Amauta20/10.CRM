from datetime import datetime

class Opportunity:
    def __init__(self, title, contact_id, value, stage='prospección', probability=10):
        self.id = None
        self.title = title
        self.contact_id = contact_id
        self.value = value
        self.stage = stage
        self.probability = probability
        self.close_date = None
        self.description = None
        self.assigned_to = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()