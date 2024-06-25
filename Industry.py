from Building import Building

class Industry(Building):
     def __init__(self):
        super().__init__()
        self.name = "Industry"
        self.upkeep_cost = 1
        self.profit = 2