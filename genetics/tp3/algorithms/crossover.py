from tp3.models.items import ItemType
from random import random


def _new_characters(char_1, char_2):
    return char_1.spawn(), char_2.spawn()


def _change_point(char_1, char_2, child_1, child_2, i):
    # Height, weapons, boots, helmets, gloves, armour
    if i == 0:
        child_2.height = char_1.height
        child_1.height = char_2.height
    elif i == 1:
        child_2.items[ItemType.WEAPON] = char_1.items[ItemType.WEAPON]
        child_1.items[ItemType.WEAPON] = char_2.items[ItemType.WEAPON]
    elif i == 2:
        child_2.items[ItemType.BOOTS] = char_1.items[ItemType.BOOTS]
        child_1.items[ItemType.BOOTS] = char_2.items[ItemType.BOOTS]
    elif i == 3:
        child_2.items[ItemType.HELMET] = char_1.items[ItemType.HELMET]
        child_1.items[ItemType.HELMET] = char_2.items[ItemType.HELMET]
    elif i == 4:
        child_2.items[ItemType.GLOVES] = char_1.items[ItemType.GLOVES]
        child_1.items[ItemType.GLOVES] = char_2.items[ItemType.GLOVES]
    elif i == 5:
        child_2.items[ItemType.ARMOUR] = char_1.items[ItemType.ARMOUR]
        child_1.items[ItemType.ARMOUR] = char_2.items[ItemType.ARMOUR]


def _maintain_point(char_1, char_2, child_1, child_2, i):
    # Height, weapons, boots, helmets, gloves, armour
    if i == 0:
        child_1.height = char_1.height
        child_2.height = char_2.height
    elif i == 1:
        child_1.items[ItemType.WEAPON] = char_1.items[ItemType.WEAPON]
        child_2.items[ItemType.WEAPON] = char_2.items[ItemType.WEAPON]
    elif i == 2:
        child_1.items[ItemType.BOOTS] = char_1.items[ItemType.BOOTS]
        child_2.items[ItemType.BOOTS] = char_2.items[ItemType.BOOTS]
    elif i == 3:
        child_1.items[ItemType.HELMET] = char_1.items[ItemType.HELMET]
        child_2.items[ItemType.HELMET] = char_2.items[ItemType.HELMET]
    elif i == 4:
        child_1.items[ItemType.GLOVES] = char_1.items[ItemType.GLOVES]
        child_2.items[ItemType.GLOVES] = char_2.items[ItemType.GLOVES]
    elif i == 5:
        child_1.items[ItemType.ARMOUR] = char_1.items[ItemType.ARMOUR]
        child_2.items[ItemType.ARMOUR] = char_2.items[ItemType.ARMOUR]


def one_point(char_1, char_2, items, point):
    child_1, child_2 = _new_characters(char_1, char_2)

    for i in range(5):
        if i < point:
            _change_point(char_1, char_2, child_1, child_2, i)
        else:
            _maintain_point(char_1, char_2, child_1, child_2, i)

    return child_1, child_2


def two_points(char_1, char_2, items, point_1, point_2):
    child_1, child_2 = _new_characters(char_1, char_2)

    for i in range(5):
        if i < point_1 or i >= point_2:
            _change_point(char_1, char_2, child_1, child_2, i)
        else:
            _maintain_point(char_1, char_2, child_1, child_2, i)

    return child_1, child_2


def uniform(char_1, char_2, items, probability=0.5):
    child_1, child_2 = _new_characters(char_1, char_2)

    for i in range(5):
        if random() < probability:
            _change_point(char_1, char_2, child_1, child_2, i)

    return child_1, child_2


def anular(char_1, char_2, items):
    child_1, child_2 = _new_characters(char_1, char_2)
    # TODO
    return child_1, child_2


#TODO completar el diccionario
crossover_function_dictionary = {
    'one_point': one_point,
    'two_points': two_points,
    'uniform': uniform,
    'anular': anular,
}