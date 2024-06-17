import Building

class Residential(Building):
     def __init__(self):
        super().__init__()
        self.name = "Residential"
        self.upkeep_cost = 0
        self.profit = 1