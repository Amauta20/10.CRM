import tkinter as tk
from tkinter import ttk, messagebox
from CRM_System.controllers.tag_controller import TagController
from CRM_System.views.tag_assignment_view import TagAssignmentDialog

class ContactDialog(tk.Toplevel):
    def __init__(self, parent, i18n, contact_controller, tag_controller, contact=None):
        super().__init__(parent)
        self.parent = parent
        self.i18n = i18n
        self.contact_controller = contact_controller
        self.tag_controller = tag_controller
        self.contact = contact
        self.title(self.i18n.get("contact_dialog", "title_add") if contact is None else self.i18n.get("contact_dialog", "title_edit"))
        self.geometry("400x400") # Increased height to accommodate new widgets
        self.create_widgets()
        self.load_contact_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "name_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "company_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.company_entry = ttk.Entry(self.frame, width=40)
        self.company_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "email_label")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(self.frame, width=40)
        self.email_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "phone_label")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(self.frame, width=40)
        self.phone_entry.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "job_title_label")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.job_title_entry = ttk.Entry(self.frame, width=40)
        self.job_title_entry.grid(row=4, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "company_level_label")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.company_level_entry = ttk.Entry(self.frame, width=40)
        self.company_level_entry.grid(row=5, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "referred_by_label")).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.referred_by_entry = ttk.Entry(self.frame, width=40)
        self.referred_by_entry.grid(row=6, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "status_label")).grid(row=7, column=0, sticky=tk.W, pady=5)
        self.status_combobox = ttk.Combobox(self.frame, values=["Cliente potencial", "Prospecto", "Cliente", "Inactivo"], width=37)
        self.status_combobox.grid(row=7, column=1, sticky=tk.W)

        # Tag selection with Listbox
        ttk.Label(self.frame, text=self.i18n.get("contact_dialog", "tags_label")).grid(row=8, column=0, sticky=tk.NW, pady=5)
        
        tags_listbox_frame = ttk.Frame(self.frame)
        tags_listbox_frame.grid(row=8, column=1, sticky=tk.W+tk.E, pady=5)

        self.tags_listbox = tk.Listbox(tags_listbox_frame, selectmode=tk.MULTIPLE, height=5)
        self.tags_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tags_scrollbar = ttk.Scrollbar(tags_listbox_frame, orient=tk.VERTICAL, command=self.tags_listbox.yview)
        tags_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tags_listbox.config(yscrollcommand=tags_scrollbar.set)

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text=self.i18n.get("contact_dialog", "save_button"), command=self.save_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("contact_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    

    def _load_tags_into_listbox(self):
        self.tags_listbox.delete(0, tk.END)
        all_tags = self.tag_controller.get_all_tags()
        self.all_tags_map = {tag.name: tag.id for tag in all_tags} # Store tag name to ID mapping

        assigned_tag_names = set()
        if self.contact and self.contact.id:
            assigned_tags = self.tag_controller.get_tags_for_contact(self.contact.id)
            assigned_tag_names = {tag['name'] for tag in assigned_tags}

        for i, tag in enumerate(all_tags):
            self.tags_listbox.insert(tk.END, tag.name)
            if tag.name in assigned_tag_names:
                self.tags_listbox.selection_set(i)

    def load_contact_data(self):
        if self.contact:
            self.name_entry.insert(0, f"{self.contact.first_name} {self.contact.last_name}")
            self.company_entry.insert(0, self.contact.company if self.contact.company else "")
            self.job_title_entry.insert(0, self.contact.job_title if self.contact.job_title else "")
            self.company_level_entry.insert(0, self.contact.company_level if self.contact.company_level else "")
            self.referred_by_entry.insert(0, self.contact.referred_by if self.contact.referred_by else "")
            self.email_entry.insert(0, self.contact.email if self.contact.email else "")
            self.phone_entry.insert(0, self.contact.phone if self.contact.phone else "")
            self.status_combobox.set(self.contact.status if self.contact.status else "")
        self._load_tags_into_listbox()

    def save_contact(self):
        name = self.name_entry.get()
        company = self.company_entry.get()
        job_title = self.job_title_entry.get()
        company_level = self.company_level_entry.get()
        referred_by = self.referred_by_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        status = self.status_combobox.get()

        if not name or not email:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("contact_dialog", "error_message"))
            return

        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        contact_data = {
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
            "job_title": job_title,
            "email": email,
            "phone": phone,
            "status": status,
            "company_level": company_level,
            "referred_by": referred_by
        }

        if self.contact:
            self.contact_controller.update_contact(self.contact.id, contact_data)
            contact_id = self.contact.id
        else:
            contact_id = self.contact_controller.create_contact(contact_data)
        
        # Handle tag assignments from listbox
        selected_tag_names = [self.tags_listbox.get(i) for i in self.tags_listbox.curselection()]
        selected_tag_ids = [self.all_tags_map[name] for name in selected_tag_names]
        self.tag_controller.set_tags_for_contact(contact_id, selected_tag_ids)

        self.parent.load_contacts()
        self.destroy()

    