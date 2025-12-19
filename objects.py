class Inventory:
    """
    Inventory Class
    """
    def __init__(self):
        self.total_storage_length = 25
        self.active_items_storage = 5
        self.passive_items_storage = 20

        self.active_items = [None for _ in range(self.active_items_storage)]
        self.passive_items = [None for _ in range(self.passive_items_storage)]

        self.inventory = {"ACTIVE ITEMS": self.active_items, "PASSIVE ITEMS": self.passive_items}
    
    def print_active_items(self):
        st = ""
        st += list(self.inventory.keys())[0]
        st += ":- \n"
        for i in self.inventory["ACTIVE ITEMS"]:
            st += f"{i} |"
        return st
    
    def print_passive_items(self):
        s = ""
        s += list(self.inventory.keys())[1]
        s += ":- \n"
        count = 1
        for i in self.inventory["PASSIVE ITEMS"]:
            if count % 5 != 0:
                s += f"{i} |"
            if count % 5 == 0:
                s += f"{i} |"
                s += "\n"
            count += 1
        return s

    def __repr__(self):
        res  = ""
        res += "\n~~INVENTORY~~"
        res += "\n"
        res += self.print_active_items()
        res += "\n"
        res += self.print_passive_items()
        res += "\n"
        
        return res
    
    def insert_item(self, item):
        if not all(self.active_items):
            for i in range(self.active_items_storage):
                if self.active_items[i] == None:
                    self.active_items[i] = item
                    break
        elif not all(self.passive_items):
            for i in range(self.passive_items_storage):
                if self.passive_items[i] == None:
                    self.passive_items[i] = item
                    break
        else:
            raise Exception("Inventory is full")


class Player:
    """
    Player Class
    """
    def __init__(self):
        self.HP = 100
        self.position = [0, 0]
        self.inventory = Inventory()

    def move(self, direction: str, unit: int):
        if direction.lower() == "north": 
            self.position[0] += unit
        elif direction.lower() == "south":
            self.position[0] -= unit
        elif direction.lower() == "east":
            self.position[1] += unit
        elif direction.lower() == "west":
            self.position[1] -= unit
        else:
            raise Exception("Invalid Direction")
    
    def teleport(self, pos: tuple):
        if len(pos) == 2:
            self.position[0] = pos[0]
            self.position[1] = pos[1]
        else:
            raise Exception("Invalid coordinates given")

#Testing:
I = Inventory()
I.insert_item("SWORD")
I.insert_item("SHEILD")
I.insert_item("PAPER")
print(I)