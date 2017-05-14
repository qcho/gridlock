from math import floor
from random import sample


def half(first_half=True):
    def filter_fn(to_filter):
        size = int(floor(len(to_filter) / 2))
        return to_filter[:size] if first_half else to_filter[size:]

    return filter_fn


def random(amount: int):
    def filter_fn(to_filter):
        return sample(to_filter, amount)

    return filter_fn


def skipping(amount: int=0, offset: int=0):
    def filter_fn(to_filter):
        return [item for i, item in enumerate(to_filter) if (i + offset) % (amount + 1) == 0]
    return filter_fn


def z_ordered(ascending=True):
    def order_fn(to_order):
        data = sorted(to_order, key=lambda x: x[2])
        return data if not ascending else reversed(data)
    return order_fn

