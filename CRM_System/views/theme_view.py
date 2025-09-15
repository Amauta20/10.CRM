import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

class ThemeDialog(tk.Toplevel):
    def __init__(self, parent, i18n, theme_controller, theme=None):
        super().__init__(parent)
        self.parent = parent
        self.i18n = i18n
        self.theme_controller = theme_controller
        self.theme = theme

        if self.theme:
            self.title(self.i18n.get("theme_dialog", "edit_title"))
        else:
            self.title(self.i18n.get("theme_dialog", "new_title"))

        self.geometry("400x500")
        self.create_widgets()
        self.load_theme_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "name_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "bg_color_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bg_color_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("bg_color"))
        self.bg_color_button.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "fg_color_label")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fg_color_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("fg_color"))
        self.fg_color_button.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "tree_bg_label")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tree_bg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("tree_bg"))
        self.tree_bg_button.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "tree_fg_label")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.tree_fg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("tree_fg"))
        self.tree_fg_button.grid(row=4, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "tree_selected_label")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.tree_selected_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("tree_selected"))
        self.tree_selected_button.grid(row=5, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "heading_bg_label")).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.heading_bg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("heading_bg"))
        self.heading_bg_button.grid(row=6, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "heading_fg_label")).grid(row=7, column=0, sticky=tk.W, pady=5)
        self.heading_fg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("heading_fg"))
        self.heading_fg_button.grid(row=7, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "button_bg_label")).grid(row=8, column=0, sticky=tk.W, pady=5)
        self.button_bg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("button_bg"))
        self.button_bg_button.grid(row=8, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "button_active_bg_label")).grid(row=9, column=0, sticky=tk.W, pady=5)
        self.button_active_bg_button = tk.Button(self.frame, text=self.i18n.get("theme_dialog", "select_color_button"), command=lambda: self.choose_color("button_active_bg"))
        self.button_active_bg_button.grid(row=9, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("theme_dialog", "relief_label")).grid(row=10, column=0, sticky=tk.W, pady=5)
        self.relief_combo = ttk.Combobox(self.frame, values=["flat", "raised", "sunken", "groove", "ridge"], width=37)
        self.relief_combo.grid(row=10, column=1, sticky=tk.W)

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text=self.i18n.get("theme_dialog", "save_button"), command=self.save_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("theme_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.colors = {}

    def choose_color(self, color_key):
        color_code = colorchooser.askcolor(title=self.i18n.get("theme_dialog", "select_color_button"))
        if color_code:
            self.colors[color_key] = color_code[1]
            getattr(self, f"{color_key}_button").config(bg=color_code[1])

    def load_theme_data(self):
        if self.theme:
            self.name_entry.insert(0, self.theme["name"])
            self.colors = self.theme["colors"]
            self.relief_combo.set(self.theme["relief"])
            for color_key, color_value in self.colors.items():
                getattr(self, f"{color_key}_button").config(bg=color_value)

    def save_theme(self):
        name = self.name_entry.get()
        relief = self.relief_combo.get()

        if not name:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("theme_dialog", "name_required_error"))
            return

        theme_data = {
            "name": name,
            "colors": self.colors,
            "relief": relief
        }

        if self.theme:
            self.theme_controller.update_theme(self.theme["name"], theme_data)
        else:
            self.theme_controller.create_theme(theme_data)
        
        self.parent.load_themes()
        self.destroy()
