import json
from typing import Dict


class JsonStorage:
    @staticmethod
    def get(model_name: str, id: int) -> Dict:
        try:
            with open(f"{model_name}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get(str(id))
        except FileNotFoundError:
            return None

    @staticmethod
    def save(model_name: str, id: int, data: Dict):
        try:
            with open(f"{model_name}.json", "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        existing_data[str(id)] = data

        with open(f"{model_name}.json", "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False)

    @staticmethod
    def delete(model_name: str, id: int):
        try:
            with open(f"{model_name}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                data.pop(str(id), None)
        except FileNotFoundError:
            return

        with open(f"{model_name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    @staticmethod
    def all(model_name: str):
        try:
            with open(f"{model_name}.json", "r", encoding="utf-8") as file:
                return json.load(file).values()
        except FileNotFoundError:
            return []
