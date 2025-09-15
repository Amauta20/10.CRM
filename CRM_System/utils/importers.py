import csv
import json

class Importer:
    @staticmethod
    def import_from_csv(filepath):
        data_dicts = []
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_dicts.append(row)
        return data_dicts

    @staticmethod
    def import_from_json(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data