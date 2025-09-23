import tkinter as tk
from tkinter import ttk, messagebox, colorchooser

def translate_color(color_name):
    color_map = {
        "rojo": "#FF0000",
        "verde": "#00FF00",
        "azul": "#0000FF",
        "amarillo": "#FFFF00",
        "naranja": "#FFA500",
        "morado": "#800080",
        "negro": "#000000",
        "blanco": "#FFFFFF",
        "gris": "#808080"
    }
    return color_map.get(color_name.lower(), color_name)

class TagDialog(tk.Toplevel):
    def __init__(self, parent, tag_controller, i18n, tag=None):
        super().__init__(parent)
        self.parent = parent
        self.tag_controller = tag_controller
        self.i18n = i18n
        self.tag = tag
        self.selected_color = "#FFFFFF"

        if self.tag:
            self.title(self.i18n.get("tag_dialog", "edit_title"))
            self.selected_color = translate_color(self.tag.color if self.tag.color else '#FFFFFF')
        else:
            self.title(self.i18n.get("tag_dialog", "new_title"))

        self.geometry("300x200")
        self.create_widgets()
        self.load_tag_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text=self.i18n.get("tag_dialog", "name_label")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame, text=self.i18n.get("tag_dialog", "color_label")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color_button = tk.Button(self.frame, text=self.i18n.get("tag_dialog", "select_color_button"), command=self.choose_color, relief=tk.FLAT, bg=self.selected_color)
        self.color_button.grid(row=1, column=1, sticky=tk.W)

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text=self.i18n.get("tag_dialog", "save_button"), command=self.save_tag).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.i18n.get("tag_dialog", "cancel_button"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Seleccionar Color")
        if color_code:
            self.selected_color = color_code[1]
            self.color_button.config(bg=self.selected_color)

    def load_tag_data(self):
        if self.tag:
            self.name_entry.insert(0, self.tag.name if self.tag.name else '')

    def save_tag(self):
        name = self.name_entry.get()
        color = self.selected_color

        if not name:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("tag_dialog", "error_message"))
            return

        try:
            tag_data = {
                "name": name,
                "color": color
            }
            if self.tag:
                self.tag_controller.update_tag(self.tag.id, tag_data)
            else:
                self.tag_controller.create_tag(tag_data)
            
            self.parent.load_tags()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
