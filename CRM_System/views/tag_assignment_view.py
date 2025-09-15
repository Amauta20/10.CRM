import tkinter as tk
from tkinter import ttk, messagebox

class TagAssignmentDialog(tk.Toplevel):
    def __init__(self, parent, i18n, tag_controller, contact_id, assigned_tags):
        super().__init__(parent)
        self.parent = parent
        self.i18n = i18n
        self.tag_controller = tag_controller
        self.contact_id = contact_id
        self.assigned_tags = {tag['id'] for tag in assigned_tags} # Store assigned tag IDs for quick lookup
        self.selected_tags = set(self.assigned_tags) # Initialize selected tags with assigned tags

        self.title(self.i18n.get("tag_assignment_dialog", "title"))
        self.geometry("300x400")
        self.create_widgets()
        self.load_tags()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("tag_assignment_dialog", "instructions")).pack(pady=5)

        self.tags_listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=40, height=10)
        self.tags_listbox.pack(pady=10)
        self.tags_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text=self.i18n.get("tag_assignment_dialog", "save_button"), command=self.save_assignments).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("tag_assignment_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def load_tags(self):
        self.all_tags = self.tag_controller.get_all_tags()
        self.tags_listbox.delete(0, tk.END)
        for i, tag in enumerate(self.all_tags):
            self.tags_listbox.insert(tk.END, tag['name'])
            if tag['id'] in self.assigned_tags:
                self.tags_listbox.selection_set(i)

    def on_listbox_select(self, event):
        self.selected_tags = set()
        for i in self.tags_listbox.curselection():
            self.selected_tags.add(self.all_tags[i]['id'])

    def save_assignments(self):
        tags_to_assign = list(self.selected_tags - self.assigned_tags)
        tags_to_remove = list(self.assigned_tags - self.selected_tags)

        for tag_id in tags_to_assign:
            self.tag_controller.assign_tag_to_contact(self.contact_id, tag_id)
        
        for tag_id in tags_to_remove:
            self.tag_controller.remove_tag_from_contact(self.contact_id, tag_id)

        self.parent.load_tags_display() # Refresh the tags display in ContactDialog
        self.parent.parent.load_contacts() # Refresh the main contacts list
        self.destroy()
