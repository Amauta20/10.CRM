from CRM_System.models.contact import Contact
from CRM_System.controllers.database_controller import DatabaseController

class ContactController:
    def __init__(self, user):
        self.db_controller = DatabaseController()
        self.current_user = user

    def create_contact(self, contact_data):
        query = """
            INSERT INTO contacts (user_id, first_name, last_name, company, job_title, email, phone, mobile_phone, address, city, state, country, postal_code, website, source, status, notes, company_level, referred_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            self.current_user.id,
            contact_data.get('first_name', ''),
            contact_data.get('last_name', ''),
            contact_data.get('company', ''),
            contact_data.get('job_title', ''),
            contact_data.get('email', ''),
            contact_data.get('phone', ''),
            contact_data.get('mobile_phone', ''),
            contact_data.get('address', ''),
            contact_data.get('city', ''),
            contact_data.get('state', ''),
            contact_data.get('country', ''),
            contact_data.get('postal_code', ''),
            contact_data.get('website', ''),
            contact_data.get('source', ''),
            contact_data.get('status', 'Cliente potencial'),
            contact_data.get('notes', ''),
            contact_data.get('company_level', ''),
            contact_data.get('referred_by', '')
        )
        contact_id = self.db_controller.execute_query(query, params)
        return contact_id

    def get_all_contacts(self):
        return self.db_controller.get_contacts(filters={'user_id': self.current_user.id})

    def get_contact(self, contact_id):
        # We need to ensure the user can only get their own contacts
        query = """SELECT c.*, GROUP_CONCAT(t.name) as tags
                 FROM contacts c
                 LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                 LEFT JOIN tags t ON ct.tag_id = t.id
                 WHERE c.id = ? AND c.user_id = ?
                 GROUP BY c.id"""
        params = (contact_id, self.current_user.id)
        result = self.db_controller.execute_query(query, params)
        if result:
            # This assumes _format_contact_results is a method in db_controller, which is not ideal
            # but we follow the existing pattern.
            return self.db_controller._format_contact_results(result)[0]
        return None

    def update_contact(self, contact_id, contact_data):
        query = """
            UPDATE contacts
            SET first_name = ?, last_name = ?, company = ?, job_title = ?, email = ?, phone = ?, mobile_phone = ?, address = ?, city = ?, state = ?, country = ?, postal_code = ?, website = ?, source = ?, status = ?, notes = ?, company_level = ?, referred_by = ?
            WHERE id = ? AND user_id = ?
        """
        params = (
            contact_data.get('first_name', ''),
            contact_data.get('last_name', ''),
            contact_data.get('company', ''),
            contact_data.get('job_title', ''),
            contact_data.get('email', ''),
            contact_data.get('phone', ''),
            contact_data.get('mobile_phone', ''),
            contact_data.get('address', ''),
            contact_data.get('city', ''),
            contact_data.get('state', ''),
            contact_data.get('country', ''),
            contact_data.get('postal_code', ''),
            contact_data.get('website', ''),
            contact_data.get('source', ''),
            contact_data.get('status', 'Cliente potencial'),
            contact_data.get('notes', ''),
            contact_data.get('company_level', ''),
            contact_data.get('referred_by', ''),
            contact_id,
            self.current_user.id
        )
        self.db_controller.execute_query(query, params)

    def clear_contacts(self):
        query = "DELETE FROM contacts WHERE user_id = ?"
        self.db_controller.execute_query(query, (self.current_user.id,))

    def edit_contact(self, contact_id):
        # Lógica para editar un contacto
        pass

    def delete_contact(self, contact_id):
        query = "DELETE FROM contacts WHERE id = ? AND user_id = ?"
        params = (contact_id, self.current_user.id)
        self.db_controller.execute_query(query, params)

    def search_contacts_by_name(self, name_prefix):
        query = """
            SELECT id, first_name, last_name FROM contacts
            WHERE (first_name LIKE ? OR last_name LIKE ? OR (first_name || ' ' || last_name) LIKE ?) AND user_id = ?
            LIMIT 10
        """
        params = (f"{name_prefix}%", f"{name_prefix}%", f"{name_prefix}%", self.current_user.id)
        results = self.db_controller.execute_query(query, params)
        
        if results:
            return [(row[0], f"{row[1]} {row[2]}") for row in results]
        return []