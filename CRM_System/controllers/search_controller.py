from typing import List, Dict
from CRM_System.controllers.database_controller import DatabaseController
from CRM_System.models.contact import Contact # Import the Contact model

class SearchController:
    def __init__(self, user):
        self.db_controller = DatabaseController()
        self.current_user = user

    def search_contacts(self, query: str, filters: Dict = None) -> List[Contact]:
        """Búsqueda avanzada en contactos"""
        search_terms = query.split()
        base_query = """
            SELECT c.* FROM contacts c
            WHERE c.user_id = ? AND (
        """
        
        conditions = []
        params = [self.current_user.id]
        
        for term in search_terms:
            conditions.append("""
                (c.first_name LIKE ? OR c.last_name LIKE ? 
                 OR c.company LIKE ? OR c.email LIKE ? OR c.notes LIKE ?)
            """)
            params.extend([f"%{term}%"] * 5)
        
        base_query += " OR ".join(conditions) + ")"
        
        # Aplicar filtros adicionales
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if value:
                    filter_conditions.append(f"c.{key} = ?")
                    params.append(value)
            
            if filter_conditions:
                base_query += " AND " + " AND ".join(filter_conditions)
        
        results = self.db_controller.execute_query(base_query, params)
        return self._format_contact_results(results)

    def _format_contact_results(self, results):
        contacts = []
        for row in results:
            # Adjust indices due to new user_id column at index 1
            contact = Contact(
                first_name=row[2],
                last_name=row[3],
                company=row[4],
                company_level=row[5],
                job_title=row[6],
                referred_by=row[7],
                email=row[8],
                phone=row[9]
            )
            contact.id = row[0]
            contact.mobile_phone = row[10]
            contact.address = row[11]
            contact.city = row[12]
            contact.state = row[13]
            contact.country = row[14]
            contact.postal_code = row[15]
            contact.website = row[16]
            contact.source = row[17]
            contact.status = row[18]
            contact.notes = row[19]
            contact.created_at = row[20]
            contact.updated_at = row[21]
            # Tags are not directly in the contact row, so we skip them here
            contacts.append(contact)
        return contacts
