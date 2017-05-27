import numpy as np
from random import uniform
from ..items.item import Item
from ..stats import Stats


class Character:

    attack_modifier_function = lambda h: 0.5 - (3*h - 5)**4 + (3*h - 5)**2 + h/2
    defense_modifier_function = lambda h: 2 + (3*h - 5)**4 - (3*h - 5)**2 - h/2
    special_modifiers = None
    default_special_modifiers = {
        'special_strength': 1.0,
        'special_agility': 1.0,
        'special_expertise': 1.0,
        'special_resistance': 1.0,
        'special_life': 1.0,
    }

    def __init__(self):
        super().__init__()
        self.items = {}
        self.height = uniform(1.3, 2.0)
        self.attack_modifier = Character.attack_modifier_function(self.height)
        self.defense_modifier = Character.defense_modifier_function(self.height)

    @staticmethod
    def set_special_modifiers(special_modifiers):
        Character.special_modifiers = {
            Stats.strength.name: special_modifiers['special_strength'],
            Stats.agility.name: special_modifiers['special_agility'],
            Stats.expertise.name: special_modifiers['special_expertise'],
            Stats.resistance.name: special_modifiers['special_resistance'],
            Stats.life.name: special_modifiers['special_life'],
        }

    def add_item(self, item: Item):
        self.items[item.type.name] = item

    def _items_properties_sum(self, function):
        return np.sum(list(map(function, self.items.values())))

    def get_strength(self):
        return 100 * np.tanh(0.01 * self._items_properties_sum(lambda x: x.strength) * self.special_modifiers[Stats.strength.name])

    def get_agility(self):
        return np.tanh(0.01 * self._items_properties_sum(lambda x: x.agility) * self.special_modifiers[Stats.agility.name])

    def get_expertise(self):
        return 0.6 * np.tanh(0.01 * self._items_properties_sum(lambda x: x.expertise) * self.special_modifiers[Stats.expertise.name])

    def get_resistance(self):
        return np.tanh(0.01 * self._items_properties_sum(lambda x: x.resistance) * self.special_modifiers[Stats.resistance.name])

    def get_life(self):
        return 100 * np.tanh(0.01 * self._items_properties_sum(lambda x: x.life) * self.special_modifiers[Stats.life.name])

    def get_attack(self):
        return (self.get_agility() + self.get_expertise()) * self.get_strength() * self.attack_modifier

    def get_defense(self):
        return (self.get_resistance() + self.get_expertise()) * self.get_life() * self.defense_modifier

    def spawn(self):
        return Character()

