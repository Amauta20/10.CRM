from typing import List, Dict
from CRM_System.controllers.database_controller import DatabaseController

class SearchController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def search_contacts(self, query: str, filters: Dict = None) -> List[Dict]:
        """Búsqueda avanzada en contactos"""
        search_terms = query.split()
        base_query = """
            SELECT c.* FROM contacts c
            WHERE (
        """
        
        conditions = []
        params = []
        
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
            contacts.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "company": row[3],
                "job_title": row[4],
                "email": row[5],
                "phone": row[6],
                "mobile_phone": row[7],
                "address": row[8],
                "city": row[9],
                "state": row[10],
                "country": row[11],
                "postal_code": row[12],
                "website": row[13],
                "source": row[14],
                "status": row[15],
                "assigned_to": row[16],
                "notes": row[17],
                "created_at": row[18],
                "updated_at": row[19],
            })
        return contacts