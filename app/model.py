from enum import Enum
from dataclasses import dataclass, field
from typing import Self, Any
from decimal import Decimal


# The Enum classes EngineType, TyreType, CarBodyType and CarBodyColor provide a way to define and group integral constants.
class EngineType(Enum):
    DIESEL = "DIESEL"
    GASOLINE = "GASOLINE"
    LPG = "LPG"

    @classmethod
    def has_member_key(cls, k: str):
        return k in cls.__members__

class TyreType(Enum):
    WINTER = "WINTER"
    SUMMER = "SUMMER"

    @classmethod
    def has_member_key(cls, k: str):
        return k in cls.__members__

class CarBodyColor(Enum):
    BLACK = "BLACK"
    SILVER = "SILVER"
    WHITE = "WHITE"
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"

    @classmethod
    def has_member_key(cls, k: str):
        return k in cls.__members__

class CarBodyType(Enum):
    SEDAN = "SEDAN"
    HATCHBACK = "HATCHBACK"
    COMBI = "COMBI"

    @classmethod
    def has_member_key(cls, k: str):
        return k in cls.__members__

# Defining Engine, Wheel and CarBody classes.
@dataclass(frozen=True, eq=True)
class Engine:
    type: EngineType
    power: float

@dataclass(frozen=True, eq=True)
class Wheel:
    type: TyreType
    model: str
    size: int

@dataclass(frozen=True, eq=True)
class CarBody:
    color: CarBodyColor
    type: CarBodyType
    components: frozenset[str] = field(default_factory=frozenset)


# The main Car class featuring data of given car, including model, price, mileage, engine, car body and wheel.
@dataclass(frozen=True, eq=True)
class Car:
    model: str
    price: Decimal
    mileage: int
    engine: Engine
    car_body: CarBody
    wheel: Wheel

    def has_price_between(self, min_price: Decimal, max_price: Decimal) -> bool:
        return min_price <= self.price <= max_price

    def has_body_type(self, body_type: CarBodyType) -> bool:
        return self.car_body.type == body_type

    def has_engine_type(self, engine_type: EngineType) -> bool:
        return self.engine.type == engine_type


    # Method to get car data and convert to object of this class.
    @classmethod
    def get_car_from_dict(cls, data: dict[str, Any]) -> Self:
        model = data["model"]
        price = Decimal(data["price"])
        mileage = data["mileage"]
        engine_data = data["engine"]
        car_body_data = data["carBody"]
        wheel_data = data["wheel"]

        engine = Engine(engine_data["type"], engine_data["power"])
        car_body = CarBody(car_body_data["color"], car_body_data["type"], frozenset(car_body_data["components"]))
        wheel = Wheel(wheel_data["type"], wheel_data["model"], wheel_data["size"])

        return cls(model, price, mileage, engine, car_body, wheel)