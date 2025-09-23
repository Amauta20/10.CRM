from CRM_System.models.activity import Activity
from CRM_System.controllers.database_controller import DatabaseController

class ActivityController:
    def __init__(self, user):
        self.db_controller = DatabaseController()
        self.current_user = user

    def create_activity(self, activity_data):
        query = """
            INSERT INTO activities (user_id, type, subject, description, related_to, related_type, due_date, completed, completed_date, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            self.current_user.id,
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
        query = "SELECT id, type, subject, due_date, completed, priority FROM activities WHERE user_id = ?"
        params = (self.current_user.id,)
        results = self.db_controller.execute_query(query, params)
        activities = []
        if results:
            for row in results:
                # Assuming row structure is (id, user_id, type, subject, description, related_to, related_type, due_date, completed, completed_date, priority)
                activity = Activity(row[2], row[3], row[4], row[5], row[6]) # Adjusted for new row structure and existing Activity constructor
                activity.id = row[0]
                activities.append(activity)
        return activities

    def get_activity(self, activity_id):
        query = "SELECT id, type, subject, due_date, completed, priority FROM activities WHERE id = ? AND user_id = ?"
        params = (activity_id, self.current_user.id)
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
            WHERE id = ? AND user_id = ?
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
            activity_id,
            self.current_user.id
        )
        self.db_controller.execute_query(query, params)

    def clear_activities(self):
        query = "DELETE FROM activities WHERE user_id = ?"
        self.db_controller.execute_query(query, (self.current_user.id,))

    def delete_activity(self, activity_id):
        query = "DELETE FROM activities WHERE id = ? AND user_id = ?"
        params = (activity_id, self.current_user.id)
        self.db_controller.execute_query(query, params)