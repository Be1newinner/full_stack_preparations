class car:
    def __init__(self,model_value,prize_value):
        self.model=model_value
        self.prize=prize_value
   
   
ford =car("creta" ,10000000)  
suzuki=car("swift" ,2000000)   
   
print(ford.model ,ford.prize)   

print(suzuki.model,suzuki.prize)