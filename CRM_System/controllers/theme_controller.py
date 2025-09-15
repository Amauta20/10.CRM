import json
import os

class ThemeController:
    def __init__(self, themes_file='themes.json'):
        self.themes_file = os.path.join(os.path.dirname(__file__), "..", themes_file)
        self.themes = self.load_themes()

    def load_themes(self):
        if os.path.exists(self.themes_file):
            with open(self.themes_file, 'r') as f:
                return json.load(f)
        return {}

    def save_themes(self):
        with open(self.themes_file, 'w') as f:
            json.dump(self.themes, f, indent=4)

    def get_themes(self):
        return self.themes

    def create_theme(self, theme_data):
        self.themes[theme_data["name"]] = theme_data
        self.save_themes()

    def update_theme(self, theme_name, theme_data):
        if theme_name in self.themes:
            self.themes[theme_name] = theme_data
            self.save_themes()

    def delete_theme(self, theme_name):
        if theme_name in self.themes:
            del self.themes[theme_name]
            self.save_themes()
