class Inventory:
    pass

class Player:
    def __init__(self):
        self.BASE_HP = 100
        self.HP = self.BASE_HP

        self.sprite = ""
        self.inventory = Inventory()
    
    def move(self):
        ...