class Dog:
    def __init__(self, breed):
        self.breed = breed
        print(f"Creating Dog: {self.breed}.")

    def eat(self):
        print(f"The {self.breed} is eating.")

    def bark(self):
        print(f"The {self.breed} is barking.")

def main():
    buddy = Dog("batman")
    buddy.eat()
    buddy.bark()

if __name__ == "__main__":
    main()
