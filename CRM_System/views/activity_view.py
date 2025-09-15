import tkinter as tk
from tkinter import ttk, messagebox

class ActivityDialog(tk.Toplevel):
    def __init__(self, parent, activity_controller, i18n, activity=None):
        super().__init__(parent)
        self.parent = parent
        self.activity_controller = activity_controller
        self.i18n = i18n
        self.activity = activity

        if self.activity:
            self.title(self.i18n.get("activity_dialog", "edit_title"))
        else:
            self.title(self.i18n.get("activity_dialog", "new_title"))

        self.geometry("400x300")
        self.create_widgets()
        self.load_activity_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("activity_dialog", "type_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.type_combo = ttk.Combobox(self.frame, width=38, values=["Llamada", "Email", "Reunión"])
        self.type_combo.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("activity_dialog", "subject_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.subject_entry = ttk.Entry(self.frame, width=40)
        self.subject_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("activity_dialog", "due_date_label")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.due_date_entry = ttk.Entry(self.frame, width=40)
        self.due_date_entry.grid(row=2, column=1, sticky=tk.W)
        self.due_date_entry.insert(0, "YYYY-MM-DD")

        ttk.Label(self.frame, text=self.i18n.get("activity_dialog", "priority_label")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.priority_combo = ttk.Combobox(self.frame, width=38, values=["Alta", "Media", "Baja"])
        self.priority_combo.grid(row=3, column=1, sticky=tk.W)

        self.completed_var = tk.BooleanVar()
        ttk.Checkbutton(self.frame, text=self.i18n.get("activity_dialog", "completed_check"), variable=self.completed_var).grid(row=4, column=1, sticky=tk.W, pady=5)

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text=self.i18n.get("activity_dialog", "save_button"), command=self.save_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("activity_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def load_activity_data(self):
        if self.activity:
            self.type_combo.set(self.activity.get('type', ''))
            self.subject_entry.insert(0, self.activity.get('subject', ''))
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, self.activity.get('due_date', 'YYYY-MM-DD'))
            self.priority_combo.set(self.activity.get('priority', ''))
            self.completed_var.set(self.activity.get('completed', False))

    def save_activity(self):
        type = self.type_combo.get()
        subject = self.subject_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_combo.get()
        completed = self.completed_var.get()

        if not type or not subject or not due_date:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("activity_dialog", "error_message"))
            return

        activity_data = {
            "type": type,
            "subject": subject,
            "due_date": due_date,
            "priority": priority,
            "completed": completed
        }

        if self.activity:
            self.activity_controller.update_activity(self.activity['id'], activity_data)
        else:
            self.activity_controller.create_activity(activity_data)
        
        self.parent.load_activities()
        self.destroy()
