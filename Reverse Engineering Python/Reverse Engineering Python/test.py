class Person:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

class SecurityGuard(Person):  # Inheritance
    def __init__(self, name: str, shift_time: str):
        super().__init__(name)
        self.shift_time = shift_time

    def check_parking_lot(self, lot: "ParkingLot"):
        return f"Guard {self.name} is checking parking lot at {lot.location}"

class Car:
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

    def __str__(self):
        return f"Car: {self.license_plate}"

class ParkingLot:
    def __init__(self, location: str):
        self.location = location
        self.cars = []  # Aggregation Cars can exist independently of the parking lot

    def add_car(self, car: Car):
        if len(self.cars) < 10:  # Assume max capacity of 10 
            self.cars.append(car)
        else:
            print(f"Parking lot at {self.location} is full.")

    def __str__(self):
        return f"Parking Lot at {self.location}, Cars: {[car.license_plate for car in self.cars]}"

class Shift:  # Composition: A shift ties a guard to a parking lot
    def __init__(self, guard: SecurityGuard, lot: ParkingLot):
        self.guard = guard
        self.lot = lot
        self.time = guard.shift_time

    def start_shift(self):
        print(f"Shift started for {self.guard.name} at {self.lot.location}. Shift time: {self.time}")
