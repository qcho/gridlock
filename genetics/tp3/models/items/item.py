from enum import Enum


class ItemType(Enum):
    ARMOUR = 1
    BOOTS = 2
    GLOVES = 3
    HELMET = 4
    WEAPON = 5


class Item:

    def __init__(self, id: int, strength: float, agility: float, expertise: float, resistance: float, life: float):
        self._id = id
        self._strength = strength
        self._agility = agility
        self._expertise = expertise
        self._resistance = resistance
        self._life = life
        self._type = None

    @property
    def strength(self):
        return self._strength

    @property
    def agility(self):
        return self._strength

    @property
    def id(self):
        return self._id

    @property
    def expertise(self):
        return self._expertise

    @property
    def resistance(self):
        return self._resistance

    @property
    def life(self):
        return self._life

    @property
    def type(self):
        return self._type

    def __str__(self):
        return "[ {} (id: {}) S: {} | A: {} | E: {} | R: {} | L: {} ]".format(
            self.type, self.id, self.strength, self.agility, self.expertise, self.resistance, self.life)

    def __repr__(self):
        return self.__str__()
