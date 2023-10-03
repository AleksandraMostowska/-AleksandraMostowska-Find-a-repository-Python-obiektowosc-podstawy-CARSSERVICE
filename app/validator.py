from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
import re
from app.model import EngineType
from app.model import CarBodyType
from app.model import CarBodyColor
from app.model import TyreType


# The Validator class checks whether the given line matches the pattern.
# First the abstract class is initialized.

class Validator(ABC):
    @abstractmethod
    def validate(self, data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        pass


# Personalized class CarValidator to check data from files.
@dataclass
class CarValidator(Validator):
    model_regex: str
    components_regex: str
    tyre_model_regex: str

    # Main method validating data.
    def validate(self, data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        errors = {}

        if "model" not in data:
            errors |= {"model": ['not found']}
        elif not re.match(self.model_regex, data['model']):
            errors |= {"model": [f'{data["model"]} does not match pattern']}

        if "price" not in data:
            errors |= {"price": ['not found']}
        elif not isinstance(data["price"], Decimal | int) or data["price"] < 0:
            errors |= {"price": ['price value is not correct']}

        if "mileage" not in data:
            errors |= {"mileage": ['not found']}
        elif not isinstance(data["mileage"], int) or data["mileage"] < 0:
            errors |= {"mileage": ['mileage value is not correct']}

        if "engine" not in data:
            errors |= {"engine": ['not found']}
        elif not self.engine_validator(data["engine"]):
            errors |= {"engine": ['engine data not correct']}

        if "carBody" not in data:
            errors |= {"carBody": ['not found']}
        elif not self.car_body_validator(data["carBody"], self.components_regex):
            errors |= {"carBody": ['car body data not correct']}

        if "wheel" not in data:
            errors |= {"wheel": ['not found']}
        elif not self.wheel_validator(data["wheel"], self.tyre_model_regex):
            errors |= {"wheel": ['wheel data not correct']}

        return len(errors) == 0, errors


    # Method to help validate the engine.
    @staticmethod
    def engine_validator(engine_data: dict[str, str | float]) -> bool:
        if "type" not in engine_data or not EngineType.has_member_key(engine_data["type"]):
            return False

        if "power" not in engine_data or not isinstance(engine_data["power"], float):
            return False

        return True

    # Method to help validate the car body.
    @staticmethod
    def car_body_validator(car_body_data: dict[str, str | list[str]], components_regex: str) -> bool:
        if "color" not in car_body_data or not CarBodyColor.has_member_key(car_body_data["color"]):
            return False

        if "type" not in car_body_data or not CarBodyType.has_member_key(car_body_data["type"]):
            return False

        if "components" not in car_body_data:
            return False
        for c in car_body_data["components"]:
            if not re.match(components_regex, c):
                return False

        return True

    # Method to help validate the wheel.
    @staticmethod
    def wheel_validator(wheel_data: dict[str, str | int], tyre_model_regex: str) -> bool:
        if "type" not in wheel_data or not TyreType.has_member_key(wheel_data["type"]):
            return False

        if "model" not in wheel_data or not re.match(tyre_model_regex, wheel_data["model"]):
            return False

        if "size" not in wheel_data or not isinstance(wheel_data["size"], int):
            return False

        return True