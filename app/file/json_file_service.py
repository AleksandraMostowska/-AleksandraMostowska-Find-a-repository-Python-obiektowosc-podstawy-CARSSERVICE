import json
from typing import Any

# Class to work with json files and parsing data to dict.
class JsonFileService:
    @staticmethod
    def get_car_from_file(filename: str) -> dict[str, Any]:
        with open(filename, 'r') as json_file:
            data_from_file = json.load(json_file)

            return data_from_file