from Building import Building

class Park(Building):
     def __init__(self):
        super().__init__()
        self.name = "Park"
        self.upkeep_cost = 1
        self.profit = 0