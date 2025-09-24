import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from CRM_System.controllers.contact_controller import ContactController
from CRM_System.controllers.search_controller import SearchController
from CRM_System.controllers.tag_controller import TagController
from CRM_System.controllers.opportunity_controller import OpportunityController
from CRM_System.controllers.activity_controller import ActivityController
from CRM_System.controllers.data_transfer_controller import DataTransferController # New import
from CRM_System.controllers.theme_controller import ThemeController
from CRM_System.views.contact_view import ContactDialog
from CRM_System.views.tag_view import TagDialog
from CRM_System.views.opportunity_view import OpportunityDialog
from CRM_System.views.activity_view import ActivityDialog
from CRM_System.views.theme_view import ThemeDialog
from CRM_System.utils.internationalization import I18n
from CRM_System.views.pipeline_view import PipelineView
from CRM_System.views.data_transfer_dialog import DataTransferDialog # New import
from CRM_System.utils.exporters import Exporter
from CRM_System.utils.importers import Importer
from tkinter import filedialog # For file dialogs


class MainWindow(tk.Tk):
    def __init__(self, user, i18n):
        super().__init__()
        self.current_user = user
        self.i18n = i18n
        self.theme_controller = ThemeController()
        self.title(f"{self.i18n.get('main_window', 'title')} - {self.current_user.full_name}")
        self.geometry("1200x800")
        self.contact_controller = ContactController(self.current_user)
        self.search_controller = SearchController(self.current_user)
        self.tag_controller = TagController(self.current_user) # Tags are global
        self.opportunity_controller = OpportunityController(self.current_user)
        self.activity_controller = ActivityController(self.current_user)
        # Pass all relevant controllers to DataTransferController
        self.data_transfer_controller = DataTransferController({
            "contact": self.contact_controller,
            "opportunity": self.opportunity_controller,
            "activity": self.activity_controller,
            "tag": self.tag_controller
        }, self.current_user)
        
        self.create_widgets()
        self.load_contacts()
        self.load_tags()
        self.load_opportunities()
        self.load_activities()
        self.load_reports()
        self.load_themes()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command(label="Español", command=lambda: self.set_language("es"))
        language_menu.add_command(label="English", command=lambda: self.set_language("en"))

        self.design_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("main_window", "design_menu"), menu=self.design_menu)
        self.design_menu.add_command(label=self.i18n.get("main_window", "light_theme"), command=lambda: self.set_theme("light"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "dark_theme"), command=lambda: self.set_theme("dark"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "formal_soft_theme"), command=lambda: self.set_theme("formal_soft"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "formal_flat_theme"), command=lambda: self.set_theme("formal_flat"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "blueprint_theme"), command=lambda: self.set_theme("blueprint"))
        self.design_menu.add_separator()
        self.design_menu.add_command(label=self.i18n.get("main_window", "minty_fresh_theme"), command=lambda: self.set_theme("minty_fresh"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "lavender_dream_theme"), command=lambda: self.set_theme("lavender_dream"))
        self.design_menu.add_command(label=self.i18n.get("main_window", "coral_charm_theme"), command=lambda: self.set_theme("coral_charm"))
        self.design_menu.add_separator()
        self.design_menu.add_command(label=self.i18n.get("main_window", "default_theme"), command=lambda: self.set_theme("default"))

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("main_window", "tools_menu"), menu=tools_menu)
        tools_menu.add_command(label=self.i18n.get("main_window", "data_transfer_button"), command=self.show_data_transfer_dialog)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("main_window", "themes_menu"), menu=theme_menu)
        theme_menu.add_command(label=self.i18n.get("main_window", "manage_themes_button"), command=self.show_theme_dialog)

        # Panel principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure Treeview style
        self.style = ttk.Style()
        
        # Pestaña de Contactos
        self.contacts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.contacts_frame, text=self.i18n.get("main_window", "contacts_tab"))

        # Widgets for Contacts tab
        toolbar = ttk.Frame(self.contacts_frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text=self.i18n.get("main_window", "new_contact_button"), 
                  command=self.show_new_contact_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=self.i18n.get("main_window", "edit_button"), 
                  command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=self.i18n.get("main_window", "delete_button"), 
                  command=self.delete_contact).pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        ttk.Entry(toolbar, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=self.i18n.get("main_window", "search_button"), command=self.search_contacts).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=self.i18n.get("main_window", "import_contacts_button"), 
                  command=self.import_contacts).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=self.i18n.get("main_window", "export_contacts_button"), 
                  command=self.export_contacts).pack(side=tk.LEFT, padx=5)
        
        # Tabla de contactos
        columns = ('id', 'nombre', 'empresa', 'nivel_empresa', 'cargo', 'referido_por', 'email', 'teléfono', 'estado', 'tags')
        self.contacts_tree = ttk.Treeview(self.contacts_frame, columns=columns, show='headings')
        
        # Define column headings using i18n
        column_headings = {
            'id': self.i18n.get("main_window", "contact_column_id"),
            'nombre': self.i18n.get("main_window", "contact_column_name"),
            'empresa': self.i18n.get("main_window", "contact_column_company"),
            'nivel_empresa': self.i18n.get("main_window", "contact_column_company_level"),
            'cargo': self.i18n.get("main_window", "contact_column_job_title"),
            'referido_por': self.i18n.get("main_window", "contact_column_referred_by"),
            'email': self.i18n.get("main_window", "contact_column_email"),
            'teléfono': self.i18n.get("main_window", "contact_column_phone"),
            'estado': self.i18n.get("main_window", "contact_column_status"),
            'tags': self.i18n.get("main_window", "contact_column_tags")
        }

        for col in columns:
            self.contacts_tree.heading(col, text=column_headings[col])
            self.contacts_tree.column(col, width=150)
        
        self.contacts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.contacts_frame, orient=tk.VERTICAL, 
                                 command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        # Pestaña de Etiquetas
        self.tags_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tags_frame, text=self.i18n.get("main_window", "tags_tab"))

        # Widgets for Tags tab
        tags_toolbar = ttk.Frame(self.tags_frame)
        tags_toolbar.pack(fill=tk.X, pady=5)

        ttk.Button(tags_toolbar, text=self.i18n.get("main_window", "new_tag_button"), command=self.show_new_tag_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(tags_toolbar, text=self.i18n.get("main_window", "edit_tag_button"), command=self.edit_tag).pack(side=tk.LEFT, padx=5)
        ttk.Button(tags_toolbar, text=self.i18n.get("main_window", "delete_tag_button"), command=self.delete_tag).pack(side=tk.LEFT, padx=5)
        ttk.Button(tags_toolbar, text=self.i18n.get("main_window", "assign_tag_button"), command=self.assign_tag_to_contact).pack(side=tk.LEFT, padx=5)

        self.tags_tree = ttk.Treeview(self.tags_frame, columns=('id', 'name', 'color'), show='headings')
        self.tags_tree.heading('id', text='ID')
        self.tags_tree.heading('name', text='Nombre')
        self.tags_tree.heading('color', text='Color')
        self.tags_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        # Pestaña de Oportunidades
        self.opportunities_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.opportunities_frame, text=self.i18n.get("main_window", "opportunities_tab"))

        # Widgets for Opportunities tab
        opportunities_toolbar = ttk.Frame(self.opportunities_frame)
        opportunities_toolbar.pack(fill=tk.X, pady=5)

        ttk.Button(opportunities_toolbar, text=self.i18n.get("main_window", "new_opportunity_button"), command=self.show_new_opportunity_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(opportunities_toolbar, text=self.i18n.get("main_window", "edit_opportunity_button"), command=self.edit_opportunity).pack(side=tk.LEFT, padx=5)
        ttk.Button(opportunities_toolbar, text=self.i18n.get("main_window", "delete_opportunity_button"), command=self.delete_opportunity).pack(side=tk.LEFT, padx=5)

        self.forecast_label = ttk.Label(opportunities_toolbar, text=self.i18n.get("main_window", "forecast_label"))
        self.forecast_label.pack(side=tk.RIGHT, padx=5)

        self.opportunities_tree = ttk.Treeview(self.opportunities_frame, columns=('id', 'title', 'contact', 'value', 'stage', 'probability'), show='headings')
        self.opportunities_tree.heading('id', text='ID')
        self.opportunities_tree.heading('title', text='Título')
        self.opportunities_tree.heading('contact', text='Contacto')
        self.opportunities_tree.heading('value', text='Valor')
        self.opportunities_tree.heading('stage', text='Etapa')
        self.opportunities_tree.heading('probability', text='Probabilidad')
        self.opportunities_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        # Pestaña de Embudo de Ventas
        self.pipeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pipeline_frame, text=self.i18n.get("main_window", "pipeline_tab"))
        self.pipeline_view = PipelineView(self.pipeline_frame, self.opportunity_controller, self.i18n)


        # Pestaña de Informes
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text=self.i18n.get("main_window", "reports_tab"))

        # Widgets for Reports tab
        self.report_text = tk.Text(self.reports_frame, wrap=tk.WORD)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        # Pestaña de Actividades
        self.activities_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.activities_frame, text=self.i18n.get("main_window", "activities_tab"))

        # Widgets for Activities tab
        activities_toolbar = ttk.Frame(self.activities_frame)
        activities_toolbar.pack(fill=tk.X, pady=5)

        ttk.Button(activities_toolbar, text=self.i18n.get("main_window", "new_activity_button"), command=self.show_new_activity_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(activities_toolbar, text=self.i18n.get("main_window", "edit_activity_button"), command=self.edit_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(activities_toolbar, text=self.i18n.get("main_window", "delete_activity_button"), command=self.delete_activity).pack(side=tk.LEFT, padx=5)

        self.activities_tree = ttk.Treeview(self.activities_frame, columns=('id', 'type', 'subject', 'due_date', 'completed', 'priority'), show='headings')
        self.activities_tree.heading('id', text='ID')
        self.activities_tree.heading('type', text='Tipo')
        self.activities_tree.heading('subject', text='Asunto')
        self.activities_tree.heading('due_date', text='Fecha de Vencimiento')
        self.activities_tree.heading('completed', text='Completado')
        self.activities_tree.heading('priority', text='Prioridad')
        self.activities_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.set_theme("default") # Set default theme

    def set_language(self, language):
        self.i18n.set_language(language)
        self.update_ui()

    def update_ui(self):
        self.title(self.i18n.get("main_window", "title"))
        self.notebook.tab(0, text=self.i18n.get("main_window", "contacts_tab"))
        self.notebook.tab(1, text=self.i18n.get("main_window", "tags_tab"))
        self.notebook.tab(2, text=self.i18n.get("main_window", "opportunities_tab"))
        self.notebook.tab(3, text=self.i18n.get("main_window", "pipeline_tab"))
        self.notebook.tab(4, text=self.i18n.get("main_window", "reports_tab"))
        self.notebook.tab(5, text=self.i18n.get("main_window", "activities_tab"))
        self.pipeline_view.draw_pipeline() # Redraw pipeline on language change
        

    def set_theme(self, theme_name):
        if theme_name == "default":
            self.style.theme_use('winnative')
            self.configure(bg=self.style.lookup("TFrame", "background"))
            return

        themes = self.theme_controller.get_themes()
        theme = themes.get(theme_name)

        if not theme:
            themes = {
                "blueprint": {
                    "bg_color": "#FFFFFF",
                    "fg_color": "#2c3e50",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#2c3e50",
                    "tree_selected": "#e8f4fc",
                    "heading_bg": "#3498db",
                    "heading_fg": "#FFFFFF",
                    "button_bg": "#3498db",
                    "button_active_bg": "#2980b9",
                    "relief": "flat"
                },
                "light": {
                    "bg_color": "#FFFFFF",
                    "fg_color": "#000000",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#000000",
                    "tree_selected": "#0078D7",
                    "heading_bg": "#F0F0F0",
                    "heading_fg": "#000000",
                    "button_bg": "#E1E1E1",
                    "button_active_bg": "#C0C0C0",
                    "relief": "raised"
                },
                "dark": {
                    "bg_color": "#2E2E2E",
                    "fg_color": "#FFFFFF",
                    "tree_bg": "#3C3C3C",
                    "tree_fg": "#FFFFFF",
                    "tree_selected": "#0078D7",
                    "heading_bg": "#505050",
                    "heading_fg": "#FFFFFF",
                    "button_bg": "#505050",
                    "button_active_bg": "#6A6A6A",
                    "relief": "raised"
                },
                "formal_soft": {
                    "bg_color": "#F5F5F5",
                    "fg_color": "#36454F",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#36454F",
                    "tree_selected": "#D4E1F5",
                    "heading_bg": "#E0E0E0",
                    "heading_fg": "#36454F",
                    "button_bg": "#E0E0E0",
                    "button_active_bg": "#C0C0C0",
                    "relief": "raised"
                },
                "formal_flat": {
                    "bg_color": "#ECECEC",
                    "fg_color": "#2C2C2C",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#2C2C2C",
                    "tree_selected": "#B0B0B0",
                    "heading_bg": "#DCDCDC",
                    "heading_fg": "#2C2C2C",
                    "button_bg": "#DCDCDC",
                    "button_active_bg": "#C8C8C8",
                    "relief": "flat"
                },
                "minty_fresh": {
                    "bg_color": "#F1F8E9",
                    "fg_color": "#333333",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#333333",
                    "tree_selected": "#C8E6C9",
                    "heading_bg": "#81C784",
                    "heading_fg": "#FFFFFF",
                    "button_bg": "#81C784",
                    "button_active_bg": "#66BB6A",
                    "relief": "flat"
                },
                "lavender_dream": {
                    "bg_color": "#F3E5F5",
                    "fg_color": "#333333",
                    "tree_bg": "#FFFFFF",
                    "tree_fg": "#333333",
                    "tree_selected": "#E1BEE7",
                    "heading_bg": "#CE93D8",
                    "heading_fg": "#FFFFFF",
                    "button_bg": "#CE93D8",
                    "button_active_bg": "#BA68C8",
                    "relief": "flat"
                },
                "coral_charm": {
                    "bg_color": "#FFF0F0",
                    "fg_color": "#333333",
                    "tree_bg": "##FFFFFF",
                    "tree_fg": "#333333",
                    "tree_selected": "#FFCDD2",
                    "heading_bg": "#F48FB1",
                    "heading_fg": "#FFFFFF",
                    "button_bg": "#F48FB1",
                    "button_active_bg": "#F06292",
                    "relief": "flat"
                }
            }
            theme = themes.get(theme_name, themes["light"])

        self.configure(bg=theme["colors"]["bg_color"])
        self.style.theme_use('default')

        # Configure styles
        self.style.configure("TFrame", background=theme["colors"]["bg_color"])
        self.style.configure("TLabel", background=theme["colors"]["bg_color"], foreground=theme["colors"]["fg_color"])
        self.style.configure("TButton", background=theme["colors"]["button_bg"], foreground=theme["colors"]["fg_color"], relief=theme["relief"], borderwidth=0 if theme["relief"] == "flat" else 1)
        self.style.map("TButton", background=[('active', theme["colors"]["button_active_bg"])])
        self.style.configure("TNotebook", background=theme["colors"]["bg_color"])
        self.style.configure("TNotebook.Tab", background=theme["colors"]["bg_color"], foreground=theme["colors"]["fg_color"])
        self.style.map("TNotebook.Tab", background=[("selected", theme["colors"]["tree_selected"])])

        # Treeview style
        self.style.configure("Treeview",
                        background=theme["colors"]["tree_bg"],
                        foreground=theme["colors"]["tree_fg"],
                        rowheight=25,
                        fieldbackground=theme["colors"]["tree_bg"])
        self.style.map('Treeview',
                  background=[('selected', theme["colors"]["tree_selected"])])

        # Treeview heading style
        self.style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background=theme["colors"]["heading_bg"],
                        foreground=theme["colors"]["heading_fg"])
        self.style.map("Treeview.Heading",
                  background=[('active', theme["colors"]["button_active_bg"])])
        self.style.map("Treeview.Heading",
                  background=[('active', theme["button_active_bg"])])

    def show_theme_dialog(self):
        dialog = ThemeDialog(self, self.i18n, self.theme_controller)
        self.wait_window(dialog)

    def show_data_transfer_dialog(self):
        # Pass all relevant controllers to the dialog
        controllers = {
            "contact": self.contact_controller,
            "opportunity": self.opportunity_controller,
            "activity": self.activity_controller,
            "tag": self.tag_controller,
            "data_transfer": self.data_transfer_controller # Pass the data transfer controller itself
        }
        dialog = DataTransferDialog(self, self.i18n, controllers)
        self.wait_window(dialog)

    def load_themes(self):
        self.themes = self.theme_controller.get_themes()
        self.design_menu.delete(11, tk.END)
        self.design_menu.add_separator()
        for theme_name in self.themes:
            self.design_menu.add_command(label=theme_name, command=lambda t=theme_name: self.set_theme(t))

    def show_new_contact_dialog(self):
        dialog = ContactDialog(self, self.i18n, self.contact_controller, self.tag_controller)
        self.wait_window(dialog)

    def edit_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("messagebox", "select_contact_error"))
            return

        contact_id = self.contacts_tree.item(selected_item, "values")[0]
        contact = self.contact_controller.get_contact(contact_id)

        dialog = ContactDialog(self, self.i18n, self.contact_controller, self.tag_controller, contact=contact)
        self.wait_window(dialog)

    def delete_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un contacto para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este contacto?"):
            contact_id = self.contacts_tree.item(selected_item, "values")[0]
            self.contact_controller.delete_contact(contact_id)
            self.load_contacts()

    def import_contacts(self):
        filepath = filedialog.askopenfilename(
            title=self.i18n.get("messagebox", "select_import_file"),
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            imported_data = Importer.import_contacts_from_csv(filepath)
            for contact_data in imported_data:
                # Need to convert dictionary to Contact object or pass to controller
                # For now, let's assume contact_controller has a method to create from dict
                self.contact_controller.create_contact_from_dict(contact_data)
            messagebox.showinfo(self.i18n.get("messagebox", "success"), self.i18n.get("messagebox", "contacts_imported_success"))
            self.load_contacts()
        except Exception as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), f"{self.i18n.get('messagebox', 'contacts_imported_error')}: {e}")

    def export_contacts(self):
        filepath = filedialog.asksaveasfilename(
            title=self.i18n.get("messagebox", "save_export_file"),
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            contacts = self.contact_controller.get_all_contacts()
            Exporter.export_contacts_to_csv(contacts, filepath)
            messagebox.showinfo(self.i18n.get("messagebox", "success"), self.i18n.get("messagebox", "contacts_exported_success"))
        except Exception as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), f"{self.i18n.get('messagebox', 'contacts_exported_error')}: {e}")

    def search_contacts(self):
        query = self.search_var.get()
        contacts = self.search_controller.search_contacts(query)
        self.contacts_tree.delete(*self.contacts_tree.get_children())
        for contact in contacts:
            tags = self.tag_controller.get_tag_names_for_contact(contact.id)
            tag_names = ", ".join(t['name'] for t in tags)
            self.contacts_tree.insert("", tk.END, values=(
                contact.id,
                f"{contact.first_name} {contact.last_name}",
                contact.company,
                contact.company_level,
                contact.job_title,
                contact.referred_by,
                contact.email,
                contact.phone,
                contact.status,
                tag_names
            ))

    def show_new_tag_dialog(self):
        dialog = TagDialog(self, self.tag_controller, self.i18n)
        self.wait_window(dialog)

    def edit_tag(self):
        selected_item = self.tags_tree.selection()
        if not selected_item:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("messagebox", "select_tag_error"))
            return

        tag_id = self.tags_tree.item(selected_item, "values")[0]
        tag = self.tag_controller.get_tag_by_id(tag_id)

        dialog = TagDialog(self, self.tag_controller, self.i18n, tag=tag)
        self.wait_window(dialog)

    def delete_tag(self):
        selected_item = self.tags_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una etiqueta para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta etiqueta?"):
            tag_id = self.tags_tree.item(selected_item, "values")[0]
            self.tag_controller.delete_tag(tag_id)
            self.load_tags()

    def assign_tag_to_contact(self):
        selected_contact_item = self.contacts_tree.selection()
        if not selected_contact_item:
            messagebox.showerror("Error", "Por favor, seleccione un contacto.")
            return

        selected_tag_item = self.tags_tree.selection()
        if not selected_tag_item:
            messagebox.showerror("Error", "Por favor, seleccione una etiqueta.")
            return

        contact_id = self.contacts_tree.item(selected_contact_item, "values")[0]
        tag_id = self.tags_tree.item(selected_tag_item, "values")[0]

        self.tag_controller.assign_tag_to_contact(contact_id, tag_id)
        self.load_contacts()

    def show_new_opportunity_dialog(self):
        dialog = OpportunityDialog(self, self.opportunity_controller, self.contact_controller, self.i18n)
        self.wait_window(dialog)

    def edit_opportunity(self):
        selected_item = self.opportunities_tree.selection()
        if not selected_item:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("messagebox", "select_opportunity_error"))
            return

        opportunity_id = self.opportunities_tree.item(selected_item, "values")[0]
        opportunity = self.opportunity_controller.get_opportunity(opportunity_id)

        dialog = OpportunityDialog(self, self.opportunity_controller, self.contact_controller, self.i18n, opportunity=opportunity)
        self.wait_window(dialog)

    def delete_opportunity(self):
        selected_item = self.opportunities_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una oportunidad para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta oportunidad?"):
            opportunity_id = self.opportunities_tree.item(selected_item, "values")[0]
            self.opportunity_controller.delete_opportunity(opportunity_id)
            self.load_opportunities()

    def show_new_activity_dialog(self):
        dialog = ActivityDialog(self, self.activity_controller, self.i18n)
        self.wait_window(dialog)

    def edit_activity(self):
        selected_item = self.activities_tree.selection()
        if not selected_item:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("messagebox", "select_activity_error"))
            return

        activity_id = self.activities_tree.item(selected_item, "values")[0]
        activity = self.activity_controller.get_activity(activity_id)

        dialog = ActivityDialog(self, self.activity_controller, self.i18n, activity=activity)
        self.wait_window(dialog)

    def delete_activity(self):
        selected_item = self.activities_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una actividad para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta actividad?"):
            activity_id = self.activities_tree.item(selected_item, "values")[0]
            self.activity_controller.delete_activity(activity_id)
            self.load_activities()

    def load_contacts(self):
        self.contacts_tree.delete(*self.contacts_tree.get_children())
        contacts = self.contact_controller.get_all_contacts()
        if contacts:
            for contact in contacts:
                tags = self.tag_controller.get_tag_names_for_contact(contact.id)
                tag_names = ", ".join(t['name'] for t in tags)
                self.contacts_tree.insert("", tk.END, values=(
                    contact.id,
                    f"{contact.first_name} {contact.last_name}",
                    contact.company,
                    contact.company_level,
                    contact.job_title,
                    contact.referred_by,
                    contact.email,
                    contact.phone,
                    contact.status,
                    tag_names
                ))

    def load_tags(self):
        self.tags_tree.delete(*self.tags_tree.get_children())
        tags = self.tag_controller.get_all_tags()
        if tags:
            for tag in tags:
                # Configure a tag for the row with the background color
                self.tags_tree.tag_configure(tag.name, background=tag.color)
                self.tags_tree.insert("", tk.END, values=(tag.id, tag.name, tag.color), tags=(tag.name,))

    def load_opportunities(self):
        self.opportunities_tree.delete(*self.opportunities_tree.get_children())
        opportunities = self.opportunity_controller.get_all_opportunities()
        if opportunities:
            for opp in opportunities:
                contact = self.contact_controller.get_contact(opp.contact_id)
                contact_name = f"{contact.first_name} {contact.last_name}" if contact else "N/A"
                self.opportunities_tree.insert("", tk.END, values=(opp.id, opp.title, contact_name, f"${opp.value:,.2f}", opp.stage, f"{opp.probability}%"))
        self.load_reports()
        self.pipeline_view.draw_pipeline() # Update pipeline when opportunities are loaded
        

    def load_activities(self):
        self.activities_tree.delete(*self.activities_tree.get_children())
        activities = self.activity_controller.get_all_activities()
        if activities:
            for act in activities:
                self.activities_tree.insert("", tk.END, values=(act.id, act.type, act.subject, act.due_date, "Sí" if act.completed else "No", act.priority))

    def load_reports(self):
        forecast = self.opportunity_controller.calculate_forecast()
        self.forecast_label.config(text=f"Pronóstico: ${forecast:,.2f}")
        
        report_text = self.opportunity_controller.generate_stage_report()
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, report_text)

    def on_closing(self):
        self.quit()

