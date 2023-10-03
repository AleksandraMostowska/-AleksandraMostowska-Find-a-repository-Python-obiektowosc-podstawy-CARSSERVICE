from app.model import CarBodyType
from app.cars_service import CarsService
from app.model import EngineType
from app.file.file_reader import CarsFileReader


def main() -> None:
    FILENAMES = ['data/AUDI.json', 'data/BMW.json', 'data/VOLVO.json', 'data/VOLVO2.json']
    validator = r'^[A-Z\s]+$'
    get_cars = CarsFileReader.get_cars(FILENAMES, validator, validator, validator)
    print(get_cars)

    cars = CarsService(get_cars)
    cars.print_all_cars()

    print(cars.sort_cars('engine power', True))

    print(cars.get_cars_by_body_and_price_range(CarBodyType.COMBI.value, 100, 120))

    print(cars.get_sorted_cars_with_engine_type(EngineType.GASOLINE.value))

    print(cars.get_statistics('mileage'))

    print(cars.get_car_mileage_pairs())

    print(cars.get_tyre_type_and_cars())

    print(cars.get_cars_with_components(["BLUETOOTH"]))



if __name__ == '__main__':
    main()