class Person:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name


class SecurityGuard(Person):
    def __init__(self, name: str, shift_time: str):
        super().__init__(name)
        self.shift_time = shift_time

    def get_shift_time(self):
        return self.shift_time


class Car:
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

    def get_license_plate(self):
        return self.license_plate


class ParkingLot:
    def __init__(self, location: str):
        self.location = location
        self.cars = []

    def get_location(self):
        return self.location

    def add_car(self, car: Car):
        self.cars.append(car)

    def get_car_count(self):
        return len(self.cars)


class Shift:
    def __init__(self, guard: SecurityGuard, lot: ParkingLot):
        self.guard = guard
        self.lot = lot

    def get_guard_name(self):
        return self.guard.get_name()

    def get_lot_location(self):
        return self.lot.get_location()
