class Car:
    def __init__(self, color, model) -> None:
        self.color = color
        self.model = model

    def start_engine(self):
        print(f"The {self.color} {self.model} engine starts")

# Creating objects
my_car = Car("red", "Toyota")
your_car = Car("blue", "Honda")

my_car.start_engine()
your_car.start_engine()

