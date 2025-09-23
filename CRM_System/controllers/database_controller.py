import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from CRM_System.models.contact import Contact

class DatabaseController:
    def __init__(self, db_path: str = 'database/crm_database.db'):
        self.db_path = 'C:\\Python\\10.CRM\\CRM_System\\database\\crm_database.db'
        self.schema_path = 'C:\\Python\\10.CRM\\CRM_System\\database\\schema.sql'
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Ejecutar script de creación de tablas
        with open(self.schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = None):
        """Ejecuta una query y retorna resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
        finally:
            conn.close()
        return result
    
    def get_contacts(self, filters: Dict = None) -> List[Dict]:
        """Obtiene contactos con filtros opcionales"""
        query = """
            SELECT c.*, GROUP_CONCAT(t.name) as tags
            FROM contacts c
            LEFT JOIN contact_tags ct ON c.id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.id
        """
        
        where_clauses = []
        params = []
        
        if filters:
            for key, value in filters.items():
                if value:
                    where_clauses.append(f"c.{key} = ?")
                    params.append(value)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " GROUP BY c.id"
        
        results = self.execute_query(query, params)
        return self._format_contact_results(results)

    def get_contact(self, contact_id):
        query = """
            SELECT c.*, GROUP_CONCAT(t.name) as tags
            FROM contacts c
            LEFT JOIN contact_tags ct ON c.id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.id
            WHERE c.id = ?
            GROUP BY c.id
        """
        params = (contact_id,)
        result = self.execute_query(query, params)
        if result:
            return self._format_contact_results(result)[0]
        return None

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
            contact.tags = row[22].split(',') if row[22] else [] # Tags are now at index 22
            contacts.append(contact)
        return contacts
