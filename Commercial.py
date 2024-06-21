import Building

class Commercial(Building):
     def __init__(self):
        super().__init__()
        self.name = "Commercial"
        self.upkeep_cost = 2
        self.profit = 3