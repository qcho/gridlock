from functools import partial
from multiprocessing.pool import Pool
import pkg_resources
from ..models.items import Item, ItemType
from ..data import __data_pkg__


def databases(dataset: str):
    with Pool(processes=8) as pool:
        return pool.map(partial(_parse_item, dataset=dataset), [
            ItemType.WEAPON,
            ItemType.BOOTS,
            ItemType.HELMET,
            ItemType.GLOVES,
            ItemType.ARMOUR,
        ])

filename = {
    ItemType.WEAPON: "armas",
    ItemType.BOOTS: "botas",
    ItemType.HELMET: "cascos",
    ItemType.GLOVES: "guantes",
    ItemType.ARMOUR: "pecheras",
}


def _parse_item(item_type: ItemType, dataset: str):
    file_name = "{}/{}.tsv".format(dataset, filename[item_type])
    with open(pkg_resources.resource_filename(__data_pkg__, file_name)) as file_handler:
        next(file_handler)
        return [(lambda x: Item(
            int(x[0]),
            float(x[1]),
            float(x[2]),
            float(x[3]),
            float(x[4]),
            float(x[5]),
            item_type))(line.split("\t"))
                for line in file_handler]
