from dataclasses import dataclass, field
from typing import Self
from decimal import Decimal
from collections import defaultdict
import statistics
from app.model import Car
from app.model import CarBodyType
from app.model import EngineType
from app.model import TyreType
from app.file.file_reader import CarsFileReader

# Cars service class is a class with all most methods and it contains list of all the cars.
@dataclass
class CarsService:
    cars: list[Car] = field(default_factory=lambda: [])

    def print_all_cars(self) -> None:
        for c in self.cars:
            print(c)

    # Sorting cars by given attribute and order.
    def sort_cars(self, sort_attribute: str, reverse_order: bool = False) -> Self:
        if sort_attribute == "components":
            return sorted(self.cars, key=lambda car: len(car.car_body.components), reverse=reverse_order)
        elif sort_attribute == "engine power":
            return sorted(self.cars, key=lambda car: car.engine.power, reverse=reverse_order)
        elif sort_attribute == "wheel size":
            return sorted(self.cars, key=lambda car: car.wheel.size, reverse=reverse_order)
        else:
            raise AttributeError("Invalid sorting key")

    # Getting all cars with specific body type and price range.
    def get_cars_by_body_and_price_range(self, body_type: CarBodyType, min_price: Decimal, max_price: Decimal) -> list[Car]:
        return [car for car in self.cars if car.has_body_type(body_type) and car.has_price_between(min_price, max_price)]

    # Sorting a list with car model names with specific engine types.
    def get_sorted_cars_with_engine_type(self, engine_type: EngineType) -> list[str]:
        return sorted([car.model for car in self.cars if car.has_engine_type(engine_type)])

    # Statistics on given attribute (price, mileage or engine power.
    def get_statistics(self, attribute: str) -> dict[str, float | int | Decimal]:
        if attribute == "price":
            values = [car.price for car in self.cars]
        elif attribute == "mileage":
            values = [car.mileage for car in self.cars]
        elif attribute == "engine power":
            values = [car.engine.power for car in self.cars]
        else:
            raise ValueError("Invalid attribute")

        if values:
            min_value = min(values)
            max_value = max(values)
            average_value = statistics.mean(values)
            return {
                "min": min_value,
                "max": max_value,
                "average": average_value
            }

        else:
            return None

    # Creating car-mileage pairs.
    def get_car_mileage_pairs(self) -> dict[Car, int]:
        return dict([(car, car.mileage) for car in self.cars])

    # Creating tyre type-car pairs.
    def get_tyre_type_and_cars(self) -> dict[TyreType, list[Car]]:
        tyre_type_and_cars = defaultdict(list)
        for car in self.cars:
            tyre_type_and_cars[car.wheel.type].append(car)

        return dict(sorted(tyre_type_and_cars.items(), key=lambda x: len(x[1]), reverse=True))

    # Getting cars with components given in argument.
    def get_cars_with_components(self, comps: list[str]) -> list[Car]:
        cars_with_components = []
        for car in self.cars:
            has_all_components = True
            for c in comps:
                if c not in car.car_body.components:
                    has_all_components = False
            if has_all_components:
                cars_with_components.append(car)

        return cars_with_components