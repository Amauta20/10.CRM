import json
import os

class I18n:
    def __init__(self, language="es"):
        self.language = language
        self.translations = self.load_translations()

    def load_translations(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "locales", f"{self.language}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, section, key):
        return self.translations.get(section, {}).get(key, f"{section}.{key}")

    def set_language(self, language):
        self.language = language
        self.translations = self.load_translations()
