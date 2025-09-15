from CRM_System.models.contact import Contact
from CRM_System.controllers.database_controller import DatabaseController

class ContactController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def create_contact(self, contact_data):
        query = """
            INSERT INTO contacts (first_name, last_name, email, phone, status)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            contact_data["first_name"],
            contact_data["last_name"],
            contact_data["email"],
            contact_data["phone"],
            contact_data["status"]
        )
        contact_id = self.db_controller.execute_query(query, params)
        return contact_id

    def create_contact_from_dict(self, contact_data):
        # Extract data, providing default empty strings for missing fields
        first_name = contact_data.get('first_name', '')
        last_name = contact_data.get('last_name', '')
        company = contact_data.get('company', '')
        job_title = contact_data.get('job_title', '')
        email = contact_data.get('email', '')
        phone = contact_data.get('phone', '')
        mobile_phone = contact_data.get('mobile_phone', '')
        address = contact_data.get('address', '')
        city = contact_data.get('city', '')
        state = contact_data.get('state', '')
        country = contact_data.get('country', '')
        postal_code = contact_data.get('postal_code', '')
        website = contact_data.get('website', '')
        source = contact_data.get('source', '')
        status = contact_data.get('status', 'Cliente potencial') # Use default from schema
        notes = contact_data.get('notes', '')

        query = """
            INSERT INTO contacts (first_name, last_name, company, job_title, email, phone, mobile_phone, address, city, state, country, postal_code, website, source, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            first_name, last_name, company, job_title, email, phone, mobile_phone, address, city, state, country, postal_code, website, source, status, notes
        )
        self.db_controller.execute_query(query, params)

    def get_all_contacts(self):
        # Lógica para obtener todos los contactos
        return self.db_controller.get_contacts()

    def get_contact(self, contact_id):
        return self.db_controller.get_contact(contact_id)

    def update_contact(self, contact_id, contact_data):
        query = """
            UPDATE contacts
            SET first_name = ?, last_name = ?, company = ?, company_level = ?, job_title = ?, referred_by = ?, email = ?, phone = ?, status = ?
            WHERE id = ?
        """
        params = (
            contact_data["first_name"],
            contact_data["last_name"],
            contact_data.get("company"),
            contact_data.get("company_level"),
            contact_data.get("job_title"),
            contact_data.get("referred_by"),
            contact_data["email"],
            contact_data["phone"],
            contact_data["status"],
            contact_id
        )
        self.db_controller.execute_query(query, params)

    def update_contact_from_dict(self, contact_id, contact_data):
        # Extract data, providing default empty strings for missing fields
        first_name = contact_data.get('first_name', '')
        last_name = contact_data.get('last_name', '')
        company = contact_data.get('company', '')
        job_title = contact_data.get('job_title', '')
        email = contact_data.get('email', '')
        phone = contact_data.get('phone', '')
        mobile_phone = contact_data.get('mobile_phone', '')
        address = contact_data.get('address', '')
        city = contact_data.get('city', '')
        state = contact_data.get('state', '')
        country = contact_data.get('country', '')
        postal_code = contact_data.get('postal_code', '')
        website = contact_data.get('website', '')
        source = contact_data.get('source', '')
        status = contact_data.get('status', 'Cliente potencial') # Use default from schema
        notes = contact_data.get('notes', '')

        query = """
            UPDATE contacts
            SET first_name = ?, last_name = ?, company = ?, job_title = ?, email = ?, phone = ?, mobile_phone = ?, address = ?, city = ?, state = ?, country = ?, postal_code = ?, website = ?, source = ?, status = ?, notes = ?
            WHERE id = ?
        """
        params = (
            first_name, last_name, company, job_title, email, phone, mobile_phone, address, city, state, country, postal_code, website, source, status, notes,
            contact_id
        )
        self.db_controller.execute_query(query, params)

    def clear_contacts(self):
        query = "DELETE FROM contacts"
        self.db_controller.execute_query(query)

    def edit_contact(self, contact_id):
        # Lógica para editar un contacto
        pass

    def delete_contact(self, contact_id):
        query = "DELETE FROM contacts WHERE id = ?"
        params = (contact_id,)
        self.db_controller.execute_query(query, params)