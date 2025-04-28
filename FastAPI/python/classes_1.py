# OOPs

# Class = blueprint of an object

# object = instance, result class

# class Car:
#     model: str = ""
#     year: int = 1990
#     company: str = ""
#     price: float = 0.0
    
# maruti = Car()

# print(maruti.company)
# print(maruti.year)


# name: str = "Vijay"
# ls: list[str] = ["Vijay", "Kumar"]

class Car:
    def __init__(self, model_value:str, price_value:float = 0):
        self.model = model_value
        self.price = price_value
        
maruti = Car("MARUTI SUZUKI", 500000)
# baleno = Car("NEXA BALENO", 1200000)
baleno = Car("NEXA BALENO")

print(maruti.model, maruti.price)
print(baleno.model, baleno.price)


