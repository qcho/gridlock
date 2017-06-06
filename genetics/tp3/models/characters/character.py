import abc

import numpy as np
import _pickle as cPickle
# from copy import deepcopy
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
        self._fitness = None
        self._strength = None
        self._agility = None
        self._expertise = None
        self._resistance = None
        self._life = None
        self._attack = None
        self._defense = None

    @staticmethod
    def set_special_modifiers(special_modifiers):
        Character.special_modifiers = {
            Stats.STRENGTH: special_modifiers['strength'],
            Stats.AGILITY: special_modifiers['agility'],
            Stats.EXPERTISE: special_modifiers['expertise'],
            Stats.RESISTANCE: special_modifiers['resistance'],
            Stats.LIFE: special_modifiers['life'],
        }

    @abc.abstractmethod
    def _calculate_fitness(self):
        pass

    def set_item(self, item: Item):
        self.items[item.type] = item

    def _items_properties_sum(self, property_fn):
        return np.sum(list(map(lambda x: property_fn.__get__(x, Item), self.items.values())))

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self._calculate_fitness()
        return self._fitness

    @property
    def strength(self):
        if self._strength is None:
            self._strength = 100 * np.tanh(
                0.01 * self._items_properties_sum(Item.strength) * self.special_modifiers[Stats.STRENGTH])
        return self._strength

    @property
    def agility(self):
        if self._agility is None:
            self._agility = np.tanh(
                0.01 * self._items_properties_sum(Item.agility) * self.special_modifiers[Stats.AGILITY])
        return self._agility

    @property
    def expertise(self):
        if self._expertise is None:
            self._expertise = 0.6 * np.tanh(
                0.01 * self._items_properties_sum(Item.expertise) * self.special_modifiers[Stats.EXPERTISE])
        return self._expertise

    @property
    def resistance(self):
        if self._resistance is None:
            self._resistance = np.tanh(
                0.01 * self._items_properties_sum(Item.resistance) * self.special_modifiers[Stats.RESISTANCE])
        return self._resistance

    @property
    def life(self):
        if self._life is None:
            self._life = 100 * np.tanh(
                0.01 * self._items_properties_sum(Item.life) * self.special_modifiers[Stats.LIFE])
        return self._life

    @property
    def attack(self):
        if self._attack is None:
            self._attack = (self.agility + self.expertise) * self.strength * self.attack_modifier
        return self._attack

    @property
    def defense(self):
        return (self.resistance + self.expertise) * self.life * self.defense_modifier

    def __str__(self):
        string = "Height: {} \nItems: \n".format(self.height)
        for x in self.items.values():
            string += str(x) + "\n"
        return string

    def spawn(self):
        child = cPickle.loads(cPickle.dumps(self, -1))
        child.invalidate_caches()
        return child

    def invalidate_caches(self):
        self._fitness = None
        self._strength = None
        self._agility = None
        self._expertise = None
        self._resistance = None
        self._life = None
        self._attack = None
        self._defense = None
