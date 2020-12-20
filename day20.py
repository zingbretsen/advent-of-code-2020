import math
import numpy as np

from copy import deepcopy
from aocd import get_data, submit


def parse_img(tile):
    return np.array([[int(cell) for cell in row] for row in tile])


def detect_sides(tile):
    img = tile["img"]
    sides = {
        "N": "".join(map(str, list(img[0, :]))),
        "S": "".join(map(str, list(img[-1, :]))),
        "E": "".join(map(str, list(img[:, -1]))),
        "W": "".join(map(str, list(img[:, 0]))),
    }
    tile["sides"] = sides
    return tile


def parse_tile(tile):
    tile = tile.replace(".", "0").replace("#", "1")
    tile = tile.split("\n")
    name = tile[0].split(" ")[1].strip(":")
    img = parse_img(tile[1:])
    tile = {"name": name, "img": img, "neighbors": []}
    tile = detect_sides(tile)
    return tile


def match_sides(tile, side_dict):
    for side in tile["sides"].values():
        if side in side_dict:
            side_dict[side].append(tile["name"])
        else:
            side_dict[side] = [tile["name"]]


from collections import defaultdict


def invert_dict(side_dict, tile_dict):
    for side, tiles in side_dict.items():
        if len(tiles) == 2:
            print(side, tiles)
            tile_dict[tiles[0]]["neighbors"].append(tiles[1])
            tile_dict[tiles[1]]["neighbors"].append(tiles[0])


def flip_tile(tile):
    tile = deepcopy(tile)
    tile["img"] = tile["img"][::-1]
    tile = detect_sides(tile)
    return tile


def rotate_tile(tile):
    tile = deepcopy(tile)
    tile["img"] = np.rot90(tile["img"])
    tile = detect_sides(tile)
    return tile


def invert_tiles(tiles):
    new_tiles = tiles[:]
    for tile in tiles:
        inverted_tile = rotate_tile(flip_tile(tile))
        inverted_tile["name"] += "_inv"
        inverted_tile["neighbors"] = []
        new_tiles.append(inverted_tile)
    return new_tiles


pairs = [["N", "S"], ["E", "W"]]


def build_image(corner, tile_dict):
    tile = tile_dict[corner]
    for neighbor in tile["neighbors"]:
        sides = tile["sides"]
        neighbor = tile_dict[neighbor]
        other_sides = neighbor["sides"]
        for s1, v1 in sides.items():
            for s2, v2 in other_sides.items():
                if v1 == v2:
                    print(s1, s2)
        tile[s1] = neighbor


if __name__ == "__main__":
    tiles = [parse_tile(tile) for tile in get_data().split("\n\n")]
    tiles = invert_tiles(tiles)

    side_dict = dict()
    tile_dict = {tile["name"]: tile for tile in tiles}

    [match_sides(tile, side_dict) for tile in tiles]

    invert_dict(side_dict, tile_dict)
    print([len(tile["neighbors"]) for tile in tile_dict.values()])
    print([tile["name"] for tile in tile_dict.values() if len(tile["neighbors"]) == 2])

    corners = [
        tile["name"]
        for tile in tile_dict.values()
        if len(tile["neighbors"]) == 2 and "inv" not in tile["name"]
    ]
    answer_a = math.prod(map(int, corners))
    print(corners)
    first_corner = corners[0]

    build_image(first_corner, tile_dict)
    # corners = ['2797', '3167', '3593', '3517']
    # 111936085519519
    submit(answer_a, part="a", day=20, year=2020)
    submit(answer_b, part="b", day=20, year=2020)
