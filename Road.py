from Building import Building

class Road(Building):
     def __init__(self):
        super().__init__()
        self.name = "Road"
        self.upkeep_cost = 1
        self.profit = 0