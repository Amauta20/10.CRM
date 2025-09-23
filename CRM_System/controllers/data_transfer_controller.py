import os
import json
from ..utils.exporters import Exporter
from ..utils.importers import Importer
from ..controllers.database_controller import DatabaseController
from ..models.contact import Contact
from ..models.opportunity import Opportunity
from ..models.activity import Activity
from ..models.tag import Tag

class DataTransferController:
    def __init__(self, controllers, user):
        self.db_controller = DatabaseController()
        self.controllers = controllers # Dictionary of other controllers (contact, opportunity, etc.)
        self.current_user = user

        # Mapping of table names to their respective model and controller for data retrieval/creation
        self.table_mappings = {
            "contacts": {
                "model": Contact,
                "get_all_method": self.controllers["contact"].get_all_contacts,
                "create_method": self.controllers["contact"].create_contact,
                "clear_method": self.controllers["contact"].clear_contacts, # Need to implement this
                "update_method": self.controllers["contact"].update_contact # Need to implement this
            },
            "opportunities": {
                "model": Opportunity,
                "get_all_method": self.controllers["opportunity"].get_all_opportunities,
                "create_method": self.controllers["opportunity"].create_opportunity, # Need to implement this
                "clear_method": self.controllers["opportunity"].clear_opportunities, # Need to implement this
                "update_method": self.controllers["opportunity"].update_opportunity # Need to implement this
            },
            "activities": {
                "model": Activity,
                "get_all_method": self.controllers["activity"].get_all_activities,
                "create_method": self.controllers["activity"].create_activity, # Need to implement this
                "clear_method": self.controllers["activity"].clear_activities, # Need to implement this
                "update_method": self.controllers["activity"].update_activity # Need to implement this
            },
            "tags": {
                "model": Tag,
                "get_all_method": self.controllers["tag"].get_all_tags,
                "create_method": self.controllers["tag"].create_tag, # Need to implement this
                "clear_method": self.controllers["tag"].clear_tags, # Need to implement this
                "update_method": self.controllers["tag"].update_tag # Need to implement this
            }
        }

    def export_data(self, selected_tables, file_format, filepath):
        all_data = {}
        for table_name in selected_tables:
            mapping = self.table_mappings.get(table_name)
            if mapping:
                data_objects = mapping["get_all_method"]()
                # Convert objects to dictionaries for export
                data_dicts = []
                for obj in data_objects:
                    obj_dict = {}
                    for attr in dir(obj):
                        if not attr.startswith('_') and not callable(getattr(obj, attr)):
                            value = getattr(obj, attr)
                            # Handle datetime objects for JSON serialization
                            if isinstance(value, (Contact, Opportunity, Activity, Tag)): # Avoid circular reference
                                continue
                            if isinstance(value, (list, dict)): # Handle nested structures if any
                                continue
                            obj_dict[attr] = str(value) if isinstance(value, (int, float, str, bool)) else value # Convert basic types to string
                    data_dicts.append(obj_dict)
                all_data[table_name] = data_dicts
            else:
                print(f"Warning: No mapping found for table {table_name}")

        if file_format == "csv":
            # For CSV, we export each table to a separate file or a single file with multiple sheets
            # For simplicity, let's export each table to a separate CSV file named after the table
            for table_name, data in all_data.items():
                if data:
                    table_filepath = os.path.join(os.path.dirname(filepath), f"{table_name}.csv")
                    Exporter.export_to_csv(data, table_filepath) # Need to modify Exporter.export_to_csv
        elif file_format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)

    def import_data(self, selected_tables, file_format, filepath, import_option):
        if file_format == "csv":
            # For CSV, we expect multiple files, one for each table
            # This is more complex. For now, let's assume a single JSON file for multi-table import
            raise NotImplementedError("CSV import for multiple tables is not yet implemented. Please use JSON.")
        elif file_format == "json":
            with open(filepath, 'r', encoding='utf-8') as f:
                all_data = json.load(f)

            # Handle clear_and_add option first
            if import_option == "clear_and_add":
                # Clear tables in reverse order of dependency to avoid foreign key issues
                for table_name in reversed(selected_tables):
                    mapping = self.table_mappings.get(table_name)
                    if mapping and mapping.get("clear_method"):
                        # Pass user_id to clear_method if it supports it
                        if table_name in ["contacts", "opportunities", "activities"]:
                            mapping["clear_method"](self.current_user.id)
                        else:
                            mapping["clear_method"]()
            
            # Import data in a specific order to respect foreign key constraints
            # Assuming a general order: tags, contacts, opportunities, activities
            import_order = ["tags", "contacts", "opportunities", "activities"]
            
            for table_name in import_order:
                if table_name in selected_tables and table_name in all_data:
                    mapping = self.table_mappings.get(table_name)
                    if mapping:
                        for item_data in all_data[table_name]:
                            # Inject user_id into item_data before creating/updating
                            if table_name in ["contacts", "opportunities", "activities"]:
                                item_data['user_id'] = self.current_user.id

                            if import_option == "append":
                                mapping["create_method"](item_data)
                            elif import_option == "replace":
                                # This assumes 'id' is present and unique in item_data
                                if 'id' in item_data and mapping.get("update_method"):
                                    mapping["update_method"](item_data['id'], item_data)
                                else:
                                    # If no update method or no ID, append
                                    mapping["create_method"](item_data)
                            elif import_option == "clear_and_add":
                                mapping["create_method"](item_data)
                    else:
                        print(f"Warning: No mapping found for table {table_name} during import.")