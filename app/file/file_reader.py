from app.file.json_file_service import JsonFileService
from app.validator import CarValidator
from app.model import Car

# Class to work with files. After validation, data is added to list.
class CarsFileReader:
    @staticmethod
    def get_cars(filenames: list[str], model_regex, components_regex, tyre_model_regex) -> list[Car]:
        all_cars = set()
        cars_validator = CarValidator(model_regex, components_regex, tyre_model_regex)

        for f in filenames:
            car_data = JsonFileService.get_car_from_file(f)
            if cars_validator.validate(car_data):
                all_cars.add(Car.get_car_from_dict(car_data))

        return list(all_cars)