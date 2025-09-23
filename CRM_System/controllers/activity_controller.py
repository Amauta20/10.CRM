from CRM_System.models.activity import Activity
from CRM_System.controllers.database_controller import DatabaseController

class ActivityController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def create_activity(self, activity_data):
        query = """
            INSERT INTO activities (type, subject, description, related_to, related_type, due_date, completed, completed_date, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            activity_data.get('type', ''),
            activity_data.get('subject', ''),
            activity_data.get('description', ''),
            activity_data.get('related_to'),
            activity_data.get('related_type', ''),
            activity_data.get('due_date'),
            activity_data.get('completed', False),
            activity_data.get('completed_date'),
            activity_data.get('priority', 'media')
        )
        self.db_controller.execute_query(query, params)

    def get_all_activities(self):
        query = "SELECT id, type, subject, due_date, completed, priority FROM activities"
        results = self.db_controller.execute_query(query)
        activities = []
        if results:
            for row in results:
                activity = Activity(row[1], row[2], row[3], row[4], row[5])
                activity.id = row[0]
                activities.append(activity)
        return activities

    def get_activity(self, activity_id):
        query = "SELECT id, type, subject, due_date, completed, priority FROM activities WHERE id = ?"
        params = (activity_id,)
        results = self.db_controller.execute_query(query, params)
        if results:
            result = results[0]
            return {
                'id': result[0],
                'type': result[1],
                'subject': result[2],
                'due_date': result[3],
                'completed': bool(result[4]),
                'priority': result[5]
            }
        return None

    def update_activity(self, activity_id, activity_data):
        query = """
            UPDATE activities
            SET type = ?, subject = ?, description = ?, related_to = ?, related_type = ?, due_date = ?, completed = ?, completed_date = ?, priority = ?
            WHERE id = ?
        """
        params = (
            activity_data.get('type', ''),
            activity_data.get('subject', ''),
            activity_data.get('description', ''),
            activity_data.get('related_to'),
            activity_data.get('related_type', ''),
            activity_data.get('due_date'),
            activity_data.get('completed', False),
            activity_data.get('completed_date'),
            activity_data.get('priority', 'media'),
            activity_id
        )
        self.db_controller.execute_query(query, params)

    def clear_activities(self):
        query = "DELETE FROM activities"
        self.db_controller.execute_query(query)

    def delete_activity(self, activity_id):
        query = "DELETE FROM activities WHERE id = ?"
        params = (activity_id,)
        self.db_controller.execute_query(query, params)