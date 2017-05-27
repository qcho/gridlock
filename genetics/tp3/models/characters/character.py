import numpy as np
from copy import deepcopy
from abc import ABCMeta
from random import uniform
from ..items.item import Item
from ..stats import Stats


class Character:
    __metaclass__ = ABCMeta

    attack_modifier_function = lambda h: 0.5 - (3 * h - 5) ** 4 + (3 * h - 5) ** 2 + h / 2
    defense_modifier_function = lambda h: 2 + (3 * h - 5) ** 4 - (3 * h - 5) ** 2 - h / 2
    special_modifiers = None
    default_special_modifiers = {
        'special_strength': 1.0,
        'special_agility': 1.0,
        'special_expertise': 1.0,
        'special_resistance': 1.0,
        'special_life': 1.0,
    }

    def __init__(self):
        self.items = {}
        self.height = uniform(1.3, 2.0)
        self.attack_modifier = Character.attack_modifier_function(self.height)
        self.defense_modifier = Character.defense_modifier_function(self.height)
        self.fitness = 0

    @staticmethod
    def set_special_modifiers(special_modifiers):
        Character.special_modifiers = {
            Stats.STRENGTH: special_modifiers['special_strength'],
            Stats.AGILITY: special_modifiers['special_agility'],
            Stats.EXPERTISE: special_modifiers['special_expertise'],
            Stats.RESISTANCE: special_modifiers['special_resistance'],
            Stats.LIFE: special_modifiers['special_life'],
        }

    def set_item(self, item: Item):
        self.items[item.type] = item

    def _items_properties_sum(self, property_fn):
        return np.sum(list(map(lambda x: property_fn.__get__(x, Item), self.items.values())))

    def get_strength(self):
        return 100 * np.tanh(
            0.01 * self._items_properties_sum(Item.strength) * self.special_modifiers[Stats.STRENGTH])

    def get_agility(self):
        return np.tanh(
            0.01 * self._items_properties_sum(Item.agility) * self.special_modifiers[Stats.AGILITY])

    def get_expertise(self):
        return 0.6 * np.tanh(
            0.01 * self._items_properties_sum(Item.expertise) * self.special_modifiers[Stats.EXPERTISE])

    def get_resistance(self):
        return np.tanh(
            0.01 * self._items_properties_sum(Item.resistance) * self.special_modifiers[Stats.RESISTANCE])

    def get_life(self):
        return 100 * np.tanh(
            0.01 * self._items_properties_sum(Item.life) * self.special_modifiers[Stats.LIFE])

    def get_attack(self):
        return (self.get_agility() + self.get_expertise()) * self.get_strength() * self.attack_modifier

    def get_defense(self):
        return (self.get_resistance() + self.get_expertise()) * self.get_life() * self.defense_modifier

    def __str__(self):
        string = "Height: {} \nItems: \n".format(self.height)
        for x in self.items:
            string = string + x.__str__() + "\n"
        return string

    def spawn(self):
        return deepcopy(self)
