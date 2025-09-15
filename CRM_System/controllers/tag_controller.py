from ..models.tag import Tag
from ..controllers.database_controller import DatabaseController

class TagController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def create_tag(self, tag_name, color='#007bff'):
        try:
            query = "INSERT INTO tags (name, color) VALUES (?, ?)"
            params = (tag_name, color)
            self.db_controller.execute_query(query, params)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("La etiqueta ya existe.")
            else:
                raise e

    def get_all_tags(self):
        query = "SELECT * FROM tags"
        results = self.db_controller.execute_query(query)
        tags = []
        for row in results:
            tag = Tag(name=row[1], color=row[2])
            tag.id = row[0]
            tags.append(tag)
        return tags

    def get_tag_by_id(self, tag_id):
        query = "SELECT * FROM tags WHERE id = ?"
        params = (tag_id,)
        results = self.db_controller.execute_query(query, params)
        if results:
            result = results[0]
            tag = Tag(name=result[1], color=result[2])
            tag.id = result[0]
            return tag
        return None

    def update_tag(self, tag_id, name, color):
        query = "UPDATE tags SET name = ?, color = ? WHERE id = ?"
        params = (name, color, tag_id)
        self.db_controller.execute_query(query, params)

    def create_tag_from_dict(self, tag_data):
        name = tag_data.get('name', '')
        color = tag_data.get('color', '#007bff')
        try:
            query = "INSERT INTO tags (name, color) VALUES (?, ?)"
            params = (name, color)
            self.db_controller.execute_query(query, params)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError("La etiqueta ya existe.")
            else:
                raise e

    def get_all_tags(self):
        query = "SELECT * FROM tags"
        results = self.db_controller.execute_query(query)
        tags = []
        for row in results:
            tag = Tag(name=row[1], color=row[2])
            tag.id = row[0]
            tags.append(tag)
        return tags

    def get_tag_by_id(self, tag_id):
        query = "SELECT * FROM tags WHERE id = ?"
        params = (tag_id,)
        results = self.db_controller.execute_query(query, params)
        if results:
            result = results[0]
            tag = Tag(name=result[1], color=result[2])
            tag.id = result[0]
            return tag
        return None

    def update_tag(self, tag_id, name, color):
        query = "UPDATE tags SET name = ?, color = ? WHERE id = ?"
        params = (name, color, tag_id)
        self.db_controller.execute_query(query, params)

    def update_tag_from_dict(self, tag_id, tag_data):
        name = tag_data.get('name', '')
        color = tag_data.get('color', '#007bff')
        query = "UPDATE tags SET name = ?, color = ? WHERE id = ?"
        params = (name, color, tag_id)
        self.db_controller.execute_query(query, params)

    def clear_tags(self):
        # First, remove associations in contact_tags table
        query_contact_tags = "DELETE FROM contact_tags WHERE tag_id IN (SELECT id FROM tags)"
        self.db_controller.execute_query(query_contact_tags)

        # Then, delete all tags
        query_tags = "DELETE FROM tags"
        self.db_controller.execute_query(query_tags)

    def delete_tag(self, tag_id):
        # First, remove associations in contact_tags table
        query_contact_tags = "DELETE FROM contact_tags WHERE tag_id = ?"
        params_contact_tags = (tag_id,)
        self.db_controller.execute_query(query_contact_tags, params_contact_tags)

        # Then, delete the tag itself
        query_tags = "DELETE FROM tags WHERE id = ?"
        params_tags = (tag_id,)
        self.db_controller.execute_query(query_tags, params_tags)

    def assign_tag_to_contact(self, contact_id, tag_id):
        query = "SELECT * FROM contact_tags WHERE contact_id = ? AND tag_id = ?"
        params = (contact_id, tag_id)
        result = self.db_controller.execute_query(query, params)
        if not result:
            query = "INSERT INTO contact_tags (contact_id, tag_id) VALUES (?, ?)"
            params = (contact_id, tag_id)
            self.db_controller.execute_query(query, params)

    def unassign_tag_from_contact(self, contact_id, tag_id):
        query = "DELETE FROM contact_tags WHERE contact_id = ? AND tag_id = ?"
        params = (contact_id, tag_id)
        self.db_controller.execute_query(query, params)

    def get_tag_names_for_contact(self, contact_id):
        query = """
            SELECT t.name, t.color
            FROM tags t
            INNER JOIN contact_tags ct ON t.id = ct.tag_id
            WHERE ct.contact_id = ?
        """
        params = (contact_id,)
        results = self.db_controller.execute_query(query, params)
        # Return a list of dictionaries, each with 'name' and 'color'
        return [{'name': row[0], 'color': row[1]} for row in results]

    def get_tags_for_contact(self, contact_id):
        query = """
            SELECT t.id, t.name, t.color
            FROM tags t
            INNER JOIN contact_tags ct ON t.id = ct.tag_id
            WHERE ct.contact_id = ?
        """
        params = (contact_id,)
        results = self.db_controller.execute_query(query, params)
        return [{'id': row[0], 'name': row[1], 'color': row[2]} for row in results]

    def set_tags_for_contact(self, contact_id, new_tag_ids):
        # Get current tags for the contact
        current_tags = self.get_tags_for_contact(contact_id)
        current_tag_ids = {tag['id'] for tag in current_tags}

        # Tags to add
        tags_to_add = [tag_id for tag_id in new_tag_ids if tag_id not in current_tag_ids]
        for tag_id in tags_to_add:
            self.assign_tag_to_contact(contact_id, tag_id)

        # Tags to remove
        tags_to_remove = [tag_id for tag_id in current_tag_ids if tag_id not in new_tag_ids]
        for tag_id in tags_to_remove:
            self.unassign_tag_from_contact(contact_id, tag_id)