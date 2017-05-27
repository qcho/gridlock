from .item import Item, ItemType


class Armour(Item):
    def __init__(self, id: int, strength: float, agility: float, expertise: float, resistance: float, life: float):
        super().__init__(id, strength, agility, expertise, resistance, life)
        self._type = ItemType.ARMOUR
