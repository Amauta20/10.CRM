import csv
import json

class Exporter:
    @staticmethod
    def export_to_csv(data_dicts, filepath):
        if not data_dicts:
            return

        # Assume all dictionaries have the same keys for headers
        headers = list(data_dicts[0].keys())

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader() # Write header row
            writer.writerows(data_dicts)

    @staticmethod
    def export_to_json(data_dicts, filepath):
        if not data_dicts:
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dicts, f, ensure_ascii=False, indent=4)