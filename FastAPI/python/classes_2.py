# OOPs 2 = Inheritance


class Vehicle:
    def __init__(self, model_value, price_value):
        self.model = model_value
        self.price = price_value

    def getModelName(self):
        # print("MODEL NAME IS ", self.model)
        print(f"MODEL NAME IS {self.model}")


class Car(Vehicle):
    def __init__(self, model_value, price_value, tyre_value=4):
        super().__init__(model_value, price_value)
        self.tyre = tyre_value


class Bike(Vehicle):
    def __init__(self, model_value, price_value, tyre_value=2):
        super().__init__(model_value, price_value)
        self.tyre = tyre_value


# maruti = Car("MARUTI SUZUKI", 500000)
baleno = Car("NEXA BALENO", 1200000)
# baleno = Car("NEXA BALENO")

# print(maruti.model, maruti.price)
print(baleno.model, baleno.price, baleno.tyre)
baleno.getModelName()

# dc = {
#     "name": "Vijay"
# }

# ls = ["VIOjay", "Kuamr"]

# dc["name"]