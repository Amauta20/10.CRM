import sqlite3
from datetime import datetime, timedelta
import random

class DummyDataGenerator:
    def __init__(self, db_path="C:\\Python\\10.CRM\\CRM_System\\database\\crm_database.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def generate_dummy_data(self):
        self.connect()
        try:
            self._clear_tables()
            self._create_dummy_tags()
            self._create_dummy_contacts()
            self._create_dummy_opportunities()
            self._create_dummy_activities()
            self._assign_dummy_contact_tags()
            print("Dummy data generated successfully.")
        except Exception as e:
            print(f"Error generating dummy data: {e}")
        finally:
            self.close()

    def _clear_tables(self):
        self.cursor.execute("DELETE FROM contact_tags")
        self.cursor.execute("DELETE FROM activities")
        self.cursor.execute("DELETE FROM opportunities")
        self.cursor.execute("DELETE FROM contacts")
        self.cursor.execute("DELETE FROM tags")
        self.conn.commit()

    def _create_dummy_tags(self):
        tags_data = [
            ("VIP", "#FF0000"),
            ("Lead", "#00FF00"),
            ("Cliente", "#0000FF"),
            ("Socio", "#FFFF00"),
            ("Potencial", "#FF00FF"),
        ]
        self.cursor.executemany("INSERT INTO tags (name, color) VALUES (?, ?)", tags_data)
        self.conn.commit()

    def _create_dummy_contacts(self):
        contact_data = [
            ("Juan", "Perez", "Tech Solutions", "Gerente", "CEO", "Maria Garcia", "juan.perez@example.com", "111-222-3333", "Cliente"),
            ("Ana", "Gomez", "Innovate Corp", "Director", "CTO", "Pedro Lopez", "ana.gomez@example.com", "444-555-6666", "Prospecto"),
            ("Carlos", "Ruiz", "Global Innovations", "Empleado", "Desarrollador", "", "carlos.ruiz@example.com", "777-888-9999", "Cliente potencial"),
            ("Laura", "Diaz", "Future Systems", "Gerente", "Project Manager", "", "laura.diaz@example.com", "123-456-7890", "Inactivo"),
            ("Pedro", "Martinez", "Dynamic Solutions", "Director", "CFO", "", "pedro.martinez@example.com", "098-765-4321", "Cliente"),
        ]
        query = "INSERT INTO contacts (first_name, last_name, company, company_level, job_title, referred_by, email, phone, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(query, contact_data)
        self.conn.commit()

    def _create_dummy_opportunities(self):
        contact_ids = [row[0] for row in self.cursor.execute("SELECT id FROM contacts").fetchall()]
        opportunities_data = []
        for _ in range(5):
            contact_id = random.choice(contact_ids)
            title = f"Proyecto {random.randint(1, 100)}"
            value = round(random.uniform(1000, 100000), 2)
            stage = random.choice(['Prospección', 'Calificación', 'Propuesta', 'Negociación', 'Cerrada Ganada', 'Cerrada Perdida'])
            probability = random.randint(10, 90)
            close_date = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            opportunities_data.append((title, contact_id, value, stage, probability, close_date))
        
        query = "INSERT INTO opportunities (title, contact_id, value, stage, probability, close_date) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(query, opportunities_data)
        self.conn.commit()

    def _create_dummy_activities(self):
        contact_ids = [row[0] for row in self.cursor.execute("SELECT id FROM contacts").fetchall()]
        activity_data = []
        for _ in range(10):
            contact_id = random.choice(contact_ids)
            activity_type = random.choice(['call', 'email', 'meeting', 'task'])
            subject = f"Seguimiento {activity_type} con Contacto {contact_id}"
            due_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
            priority = random.choice(['baja', 'media', 'alta'])
            activity_data.append((activity_type, subject, contact_id, 'contact', due_date, priority))
        
        query = "INSERT INTO activities (type, subject, related_to, related_type, due_date, priority) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(query, activity_data)
        self.conn.commit()

    def _assign_dummy_contact_tags(self):
        contact_ids = [row[0] for row in self.cursor.execute("SELECT id FROM contacts").fetchall()]
        tag_ids = [row[0] for row in self.cursor.execute("SELECT id FROM tags").fetchall()]
        contact_tag_data = []
        for contact_id in contact_ids:
            # Assign 1 to 3 random tags to each contact
            num_tags = random.randint(1, 3)
            assigned_tags = random.sample(tag_ids, min(num_tags, len(tag_ids)))
            for tag_id in assigned_tags:
                contact_tag_data.append((contact_id, tag_id))
        
        query = "INSERT INTO contact_tags (contact_id, tag_id) VALUES (?, ?)"
        self.cursor.executemany(query, contact_tag_data)
        self.conn.commit()

if __name__ == "__main__":
    generator = DummyDataGenerator()
    generator.generate_dummy_data()
