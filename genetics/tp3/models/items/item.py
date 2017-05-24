from enum import Enum

class Item:
    ItemType = Enum('ItemType', 'armour boots gloves helmet weapon')

    def __init__(self, id: int, strength: float, agility: float, expertise: float, resistance: float, life: float):
        self.id = id
        self.strength = strength
        self.agility = agility
        self.expertise = expertise
        self.resistance = resistance
        self.life = life
        self.type = 0


    def __str__(self):
        return "[ {} (id: {}) S: {} | A: {} | E: {} | R: {} | L: {} ]".format(
            self.type.name, self.id, self.strength, self.agility, self.expertise, self.resistance, self.life)


    def __repr__(self):
        return self.__str__()