from ..models.items import ItemType
from ..models.characters import Character
from random import random
from random import randint

GENES = 6


def _spawn_children(char_1, char_2):
    return char_1.spawn(), char_2.spawn()


def _swap_item(child_1: Character, child_2: Character, item_type: ItemType):
    child_1.items[item_type], child_2.items[item_type] = child_2.items[item_type], child_1.items[item_type]


def _swap_height(child_1: Character, child_2: Character):
    child_1.height, child_2.height = child_2.height, child_1.height


def one_point(char_1: Character, char_2: Character):
    point = randint(1, GENES-1)
    child_1, child_2 = _spawn_children(char_1, char_2)
    if point == 0:
        _swap_height(child_1, child_2)
    for i, item_type in enumerate(ItemType):
        if i >= point:
            _swap_item(child_1, child_2, item_type)

    return child_1, child_2


def two_points(char_1: Character, char_2: Character):
    point_1 = randint(0, GENES - 1)
    point_2 = randint(point_1, GENES - 1)
    child_1, child_2 = _spawn_children(char_1, char_2)
    if point_1 == 0:
        _swap_height(child_1, child_2)
    for i, item_type in enumerate(ItemType):
        if i < point_1 or i >= point_2:
            _swap_item(child_1, child_2, item_type)

    return child_1, child_2


def uniform(char_1: Character, char_2: Character):
    probability = 0.5
    child_1, child_2 = _spawn_children(char_1, char_2)
    if random() < probability:
        _swap_height(child_1, child_2)
    for i, item_type in enumerate(ItemType):
        if random() < probability:
            _swap_item(child_1, child_2, item_type)

    return child_1, child_2


def annular(char_1: Character, char_2: Character):
    child_1, child_2 = _spawn_children(char_1, char_2)
    point = randint(0, GENES)
    length = randint(0, GENES-1)
    for i in range(length):
        index = (point + i) % GENES
        if index == 0:
            _swap_height(child_1, child_2)
        else:
            _swap_item(child_1, child_2, ItemType(index))
    return child_1, child_2


crossover_function_dictionary = {
    'one_point': one_point,
    'two_points': two_points,
    'uniform': uniform,
    'annular': annular,
}
