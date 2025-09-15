import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class DataTransferDialog(tk.Toplevel):
    def __init__(self, parent, i18n, controllers):
        super().__init__(parent)
        self.parent = parent
        self.i18n = i18n
        self.controllers = controllers # Dictionary of all relevant controllers
        self.title(self.i18n.get("data_transfer_dialog", "title"))
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Table Selection
        ttk.Label(main_frame, text=self.i18n.get("data_transfer_dialog", "select_tables_label")).pack(anchor=tk.W)
        
        self.table_selection_frame = ttk.Frame(main_frame)
        self.table_selection_frame.pack(fill=tk.X, pady=5)

        self.tables = {
            "contacts": {"name": self.i18n.get("data_transfer_dialog", "table_contacts"), "selected": tk.BooleanVar(value=True)},
            "opportunities": {"name": self.i18n.get("data_transfer_dialog", "table_opportunities"), "selected": tk.BooleanVar(value=True)},
            "activities": {"name": self.i18n.get("data_transfer_dialog", "table_activities"), "selected": tk.BooleanVar(value=True)},
            "tags": {"name": self.i18n.get("data_transfer_dialog", "table_tags"), "selected": tk.BooleanVar(value=True)},
            # Add other tables as needed
        }

        for key, table_info in self.tables.items():
            cb = ttk.Checkbutton(self.table_selection_frame, text=table_info["name"], variable=table_info["selected"])
            cb.pack(side=tk.LEFT, padx=5)

        # Format Selection
        ttk.Label(main_frame, text=self.i18n.get("data_transfer_dialog", "select_format_label")).pack(anchor=tk.W, pady=(10, 0))
        self.format_var = tk.StringVar(value="csv")
        ttk.Radiobutton(main_frame, text="CSV", variable=self.format_var, value="csv").pack(anchor=tk.W, padx=5)
        ttk.Radiobutton(main_frame, text="JSON", variable=self.format_var, value="json").pack(anchor=tk.W, padx=5)

        # Import Options (for import only)
        ttk.Label(main_frame, text=self.i18n.get("data_transfer_dialog", "import_options_label")).pack(anchor=tk.W, pady=(10, 0))
        self.import_option_var = tk.StringVar(value="append")
        ttk.Radiobutton(main_frame, text=self.i18n.get("data_transfer_dialog", "option_append"), variable=self.import_option_var, value="append").pack(anchor=tk.W, padx=5)
        ttk.Radiobutton(main_frame, text=self.i18n.get("data_transfer_dialog", "option_replace"), variable=self.import_option_var, value="replace").pack(anchor=tk.W, padx=5)
        ttk.Radiobutton(main_frame, text=self.i18n.get("data_transfer_dialog", "option_clear_and_add"), variable=self.import_option_var, value="clear_and_add").pack(anchor=tk.W, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        ttk.Button(button_frame, text=self.i18n.get("data_transfer_dialog", "export_button"), command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("data_transfer_dialog", "import_button"), command=self.import_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("data_transfer_dialog", "cancel_button"), command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def export_data(self):
        selected_tables = [key for key, info in self.tables.items() if info["selected"].get()]
        if not selected_tables:
            messagebox.showwarning(self.i18n.get("messagebox", "warning"), self.i18n.get("data_transfer_dialog", "no_tables_selected_export"))
            return

        file_format = self.format_var.get()
        filepath = filedialog.asksaveasfilename(
            title=self.i18n.get("data_transfer_dialog", "save_export_file"),
            defaultextension=f".{file_format}",
            filetypes=[(f"{file_format.upper()} files", f"*.{file_format}"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            # Call a controller method to handle the export
            self.controllers["data_transfer"].export_data(selected_tables, file_format, filepath)
            messagebox.showinfo(self.i18n.get("messagebox", "success"), self.i18n.get("data_transfer_dialog", "export_success"))
        except Exception as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), f"{self.i18n.get('data_transfer_dialog', 'export_error')}: {e}")

    def import_data(self):
        selected_tables = [key for key, info in self.tables.items() if info["selected"].get()]
        if not selected_tables:
            messagebox.showwarning(self.i18n.get("messagebox", "warning"), self.i18n.get("data_transfer_dialog", "no_tables_selected_import"))
            return

        file_format = self.format_var.get()
        import_option = self.import_option_var.get()
        filepath = filedialog.askopenfilename(
            title=self.i18n.get("data_transfer_dialog", "select_import_file"),
            filetypes=[(f"{file_format.upper()} files", f"*.{file_format}"), ("All files", "*.*")]
        )
        if not filepath:
            return

        if not messagebox.askyesno(self.i18n.get("messagebox", "confirm"), self.i18n.get("data_transfer_dialog", "import_confirm")):
            return

        try:
            # Call a controller method to handle the import
            self.controllers["data_transfer"].import_data(selected_tables, file_format, filepath, import_option)
            messagebox.showinfo(self.i18n.get("messagebox", "success"), self.i18n.get("data_transfer_dialog", "import_success"))
            self.parent.load_contacts() # Reload data in main window
            self.parent.load_tags()
            self.parent.load_opportunities()
            self.parent.load_activities()
            self.parent.load_reports()
            self.parent.pipeline_view.draw_pipeline()
        except Exception as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), f"{self.i18n.get('data_transfer_dialog', 'import_error')}: {e}")