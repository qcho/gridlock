from models.items import Item
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
        new_character_2.items[Item.ItemType.weapon.name] = character_1.items[Item.ItemType.weapon.name]
        new_character_1.items[Item.ItemType.weapon.name] = character_2.items[Item.ItemType.weapon.name]
    elif i == 2:
        new_character_2.items[Item.ItemType.boots.name] = character_1.items[Item.ItemType.boots.name]
        new_character_1.items[Item.ItemType.boots.name] = character_2.items[Item.ItemType.boots.name]
    elif i == 3:
        new_character_2.items[Item.ItemType.helmet.name] = character_1.items[Item.ItemType.helmet.name]
        new_character_1.items[Item.ItemType.helmet.name] = character_2.items[Item.ItemType.helmet.name]
    elif i == 4:
        new_character_2.items[Item.ItemType.gloves.name] = character_1.items[Item.ItemType.gloves.name]
        new_character_1.items[Item.ItemType.gloves.name] = character_2.items[Item.ItemType.gloves.name]
    elif i == 5:
        new_character_2.items[Item.ItemType.armour.name] = character_1.items[Item.ItemType.armour.name]
        new_character_1.items[Item.ItemType.armour.name] = character_2.items[Item.ItemType.armour.name]


def _maintain_point(character_1, character_2, new_character_1, new_character_2, i):
    # Height, weapons, boots, helmets, gloves, armour
    if i == 0:
        new_character_1.height = character_1.height
        new_character_2.height = character_2.height
    elif i == 1:
        new_character_1.items[Item.ItemType.weapon.name] = character_1.items[Item.ItemType.weapon.name]
        new_character_2.items[Item.ItemType.weapon.name] = character_2.items[Item.ItemType.weapon.name]
    elif i == 2:
        new_character_1.items[Item.ItemType.boots.name] = character_1.items[Item.ItemType.boots.name]
        new_character_2.items[Item.ItemType.boots.name] = character_2.items[Item.ItemType.boots.name]
    elif i == 3:
        new_character_1.items[Item.ItemType.helmet.name] = character_1.items[Item.ItemType.helmet.name]
        new_character_2.items[Item.ItemType.helmet.name] = character_2.items[Item.ItemType.helmet.name]
    elif i == 4:
        new_character_1.items[Item.ItemType.gloves.name] = character_1.items[Item.ItemType.gloves.name]
        new_character_2.items[Item.ItemType.gloves.name] = character_2.items[Item.ItemType.gloves.name]
    elif i == 5:
        new_character_1.items[Item.ItemType.armour.name] = character_1.items[Item.ItemType.armour.name]
        new_character_2.items[Item.ItemType.armour.name] = character_2.items[Item.ItemType.armour.name]


def one_point(character_1, character_2, items, point):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if i < point:
            _change_point(character_1, character_2, new_character_1, new_character_2, items, i)
        else:
            _maintain_point(character_1, character_2, new_character_1, new_character_2, items, i)

    return (new_character_1, new_character_2)


def two_points(character_1, character_2, items, point_1, point_2):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if i < point_1 or i >= point_2:
            _change_point(character_1, character_2, new_character_1, new_character_2, items, i)
        else:
            _maintain_point(character_1, character_2, new_character_1, new_character_2, items, i)

    return (new_character_1, new_character_2)


def uniform(character_1, character_2, items, probability=0.5):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)

    for i in range(5):
        if random() < probability:
            _change_point(character_1, character_2, new_character_1, new_character_2, items, i)

    return (new_character_1, new_character_2)


def anular(character_1, character_2, items):
    new_character_1, new_character_2 = _new_characters(character_1, character_2)
    # TODO
    return (new_character_1, new_character_2)


#TODO completar el diccionario
crossover_function_dictionary = {
    'one_point': one_point,
    'two_points': two_points,
    'uniform': uniform,
    'anular': anular,
}