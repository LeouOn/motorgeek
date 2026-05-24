from motorgeek.core.models import Car

def test_car_creation():
    car = Car(make="Porsche", model="911 Turbo", generation="996", year_start=1998, year_end=2005)
    assert car.make == "Porsche"
    assert car.generation == "996"

def test_car_slug():
    car = Car(make="Porsche", model="911 Turbo", generation="996", year_start=1998, year_end=2005)
    assert car.slug == "porsche-911-turbo-996"