from enum import Enum


class ItemType(Enum):
    NONE = 0
    ARMOUR = 1
    BOOTS = 2
    GLOVES = 3
    HELMET = 4
    WEAPON = 5


class Item:

    def __init__(self, id: int, strength: float, agility: float, expertise: float, resistance: float, life: float):
        self.id = id
        self.strength = strength
        self.agility = agility
        self.expertise = expertise
        self.resistance = resistance
        self.life = life
        self.type = ItemType.NONE

    def __str__(self):
        return "[ {} (id: {}) S: {} | A: {} | E: {} | R: {} | L: {} ]".format(
            self.type.name, self.id, self.strength, self.agility, self.expertise, self.resistance, self.life)


    def __repr__(self):
        return self.__str__()