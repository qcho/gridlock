from tp3.models.items import ItemType
from random import random


def _new_characters(character_1, character_2):
    new_character_1 = character_1.spawn()
    new_character_2 = character_2.spawn()
    return new_character_1, new_character_2


def _change_point(character_1, character_2, new_character_1, new_character_2, i):
    # Height, weapons, boots, helmets, gloves, armour
    if i == 0:
        new_character_2.height = character_1.height
        new_character_1.height = character_2.height
    elif i == 1:
        new_character_2.items[ItemType.WEAPON] = character_1.items[ItemType.WEAPON]
        new_character_1.items[ItemType.WEAPON] = character_2.items[ItemType.WEAPON]
    elif i == 2:
        new_character_2.items[ItemType.BOOTS] = character_1.items[ItemType.BOOTS]
        new_character_1.items[ItemType.BOOTS] = character_2.items[ItemType.BOOTS]
    elif i == 3:
        new_character_2.items[ItemType.HELMET] = character_1.items[ItemType.HELMET]
        new_character_1.items[ItemType.HELMET] = character_2.items[ItemType.HELMET]
    elif i == 4:
        new_character_2.items[ItemType.GLOVES] = character_1.items[ItemType.GLOVES]
        new_character_1.items[ItemType.GLOVES] = character_2.items[ItemType.GLOVES]
    elif i == 5:
        new_character_2.items[ItemType.ARMOUR] = character_1.items[ItemType.ARMOUR]
        new_character_1.items[ItemType.ARMOUR] = character_2.items[ItemType.ARMOUR]


def _maintain_point(character_1, character_2, new_character_1, new_character_2, i):
    # Height, weapons, boots, helmets, gloves, armour
    if i == 0:
        new_character_1.height = character_1.height
        new_character_2.height = character_2.height
    elif i == 1:
        new_character_1.items[ItemType.WEAPON] = character_1.items[ItemType.WEAPON]
        new_character_2.items[ItemType.WEAPON] = character_2.items[ItemType.WEAPON]
    elif i == 2:
        new_character_1.items[ItemType.BOOTS] = character_1.items[ItemType.BOOTS]
        new_character_2.items[ItemType.BOOTS] = character_2.items[ItemType.BOOTS]
    elif i == 3:
        new_character_1.items[ItemType.HELMET] = character_1.items[ItemType.HELMET]
        new_character_2.items[ItemType.HELMET] = character_2.items[ItemType.HELMET]
    elif i == 4:
        new_character_1.items[ItemType.GLOVES] = character_1.items[ItemType.GLOVES]
        new_character_2.items[ItemType.GLOVES] = character_2.items[ItemType.GLOVES]
    elif i == 5:
        new_character_1.items[ItemType.ARMOUR] = character_1.items[ItemType.ARMOUR]
        new_character_2.items[ItemType.ARMOUR] = character_2.items[ItemType.ARMOUR]


def one_point(character_1, character_2, items, point):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if i < point:
            _change_point(character_1, character_2, new_character_1, new_character_2, i)
        else:
            _maintain_point(character_1, character_2, new_character_1, new_character_2, i)

    return new_character_1, new_character_2


def two_points(character_1, character_2, items, point_1, point_2):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if i < point_1 or i >= point_2:
            _change_point(character_1, character_2, new_character_1, new_character_2, i)
        else:
            _maintain_point(character_1, character_2, new_character_1, new_character_2, i)

    return new_character_1, new_character_2


def uniform(character_1, character_2, items, probability=0.5):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if random() < probability:
            _change_point(character_1, character_2, new_character_1, new_character_2, i)

    return new_character_1, new_character_2


def anular(character_1, character_2, items):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)
    # TODO
    return new_character_1, new_character_2


#TODO completar el diccionario
crossover_function_dictionary = {
    'one_point': one_point,
    'two_points': two_points,
    'uniform': uniform,
    'anular': anular,
}