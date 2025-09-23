import tkinter as tk
from tkinter import ttk, messagebox

class OpportunityDialog(tk.Toplevel):
    def __init__(self, parent, opportunity_controller, contact_controller, i18n, opportunity=None):
        super().__init__(parent)
        self.parent = parent
        self.opportunity_controller = opportunity_controller
        self.contact_controller = contact_controller
        self.i18n = i18n
        self.opportunity = opportunity

        if self.opportunity:
            self.title(self.i18n.get("opportunity_dialog", "edit_title"))
        else:
            self.title(self.i18n.get("opportunity_dialog", "new_title"))

        self.geometry("400x400")
        self.create_widgets()
        self.load_opportunity_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("opportunity_dialog", "title_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(self.frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("opportunity_dialog", "contact_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.contact_combo = ttk.Combobox(self.frame, width=38)
        self.contact_combo.grid(row=1, column=1, sticky=tk.W)
        self.contact_combo.bind('<KeyRelease>', self.on_contact_key_release)

        ttk.Label(self.frame, text=self.i18n.get("opportunity_dialog", "value_label")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.value_entry = ttk.Entry(self.frame, width=40)
        self.value_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("opportunity_dialog", "stage_label")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.stage_combo = ttk.Combobox(self.frame, width=38, values=["Prospección", "Cualificación", "Propuesta", "Negociación", "Ganado", "Perdido"])
        self.stage_combo.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("opportunity_dialog", "probability_label")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.probability_scale = ttk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=self.update_probability_label)
        self.probability_scale.grid(row=4, column=1, sticky=tk.W)

        self.probability_label = ttk.Label(self.frame, text="0%")
        self.probability_label.grid(row=4, column=2, sticky=tk.W, padx=5)

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text=self.i18n.get("opportunity_dialog", "save_button"), command=self.save_opportunity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("opportunity_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def on_contact_key_release(self, event):
        search_term = self.contact_combo.get()
        if len(search_term) > 0:
            contacts = self.contact_controller.search_contacts_by_name(search_term)
            if contacts:
                contact_names = [name for id, name in contacts]
                self.contact_combo['values'] = contact_names
                self.contacts_map = {name: id for id, name in contacts}
                # self.contact_combo.event_generate('<Down>') # This can be annoying
            else:
                self.contact_combo['values'] = []
        else:
            self.contact_combo['values'] = []

    def load_opportunity_data(self):
        if self.opportunity:
            self.title_entry.insert(0, self.opportunity.title)
            self.value_entry.insert(0, self.opportunity.value)
            self.stage_combo.set(self.opportunity.stage)
            self.probability_scale.set(self.opportunity.probability)
            self.update_probability_label(self.opportunity.probability)
            
            contact = self.contact_controller.get_contact(self.opportunity.contact_id)
            if contact:
                contact_full_name = f"{contact.first_name} {contact.last_name}"
                self.contact_combo.set(contact_full_name)
                # We need to ensure the initial contact is in the map for saving without changes
                self.contacts_map[contact_full_name] = contact.id

    def update_probability_label(self, value):
        self.probability_label.config(text=f"{int(float(value))}")

    def save_opportunity(self):
        title = self.title_entry.get()
        contact_name = self.contact_combo.get()
        value = self.value_entry.get()
        stage = self.stage_combo.get()
        probability = self.probability_scale.get()

        if not title or not contact_name or not value or not stage:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("opportunity_dialog", "error_message"))
            return

        try:
            value = float(value)
        except ValueError:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("opportunity_dialog", "value_error_message"))
            return

        contact_id = self.contacts_map.get(contact_name)

        if not contact_id:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("opportunity_dialog", "contact_not_found_error"))
            return

        opportunity_data = {
            "title": title,
            "contact_id": contact_id,
            "value": value,
            "stage": stage,
            "probability": int(probability)
        }

        if self.opportunity:
            self.opportunity_controller.update_opportunity(self.opportunity.id, opportunity_data)
        else:
            self.opportunity_controller.create_opportunity(opportunity_data)
        
        self.parent.load_opportunities()
        self.destroy()
