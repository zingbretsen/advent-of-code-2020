import math
import numpy as np

from copy import deepcopy
from aocd import get_data, submit

from scipy import ndimage


def parse_img(tile):
    return np.array([[int(cell) for cell in row] for row in tile])


def detect_sides(tile):
    img = tile["img"]
    sides = {
        "N": tuple(
            sorted(
                [
                    "".join(map(str, list(img[0, :]))),
                    "".join(map(str, list(img[0, :])))[::-1],
                ]
            )
        ),
        "S": tuple(
            sorted(
                [
                    "".join(map(str, list(img[-1, :]))),
                    "".join(map(str, list(img[-1, :])))[::-1],
                ]
            )
        ),
        "E": tuple(
            sorted(
                [
                    "".join(map(str, list(img[:, -1]))),
                    "".join(map(str, list(img[:, -1])))[::-1],
                ]
            )
        ),
        "W": tuple(
            sorted(
                [
                    "".join(map(str, list(img[:, 0]))),
                    "".join(map(str, list(img[:, 0])))[::-1],
                ]
            )
        ),
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
            tile_dict[tiles[0]]["neighbors"].append(tiles[1])
            tile_dict[tiles[1]]["neighbors"].append(tiles[0])


def flip_tile(tile, direction="horizontal"):
    tile = deepcopy(tile)
    if direction == "vertical":
        tile["img"] = tile["img"][::-1, :]
    elif direction == "horizontal":
        tile["img"] = tile["img"][:, ::-1]
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


pairs = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}


def find_neighbor_in_dir(tile, tile_dict, direction="E"):
    tile = detect_sides(tile)
    for neighbor in tile["neighbors"]:
        sides = tile["sides"]
        neighbor = detect_sides(tile_dict[neighbor])
        other_sides = neighbor["sides"]
        s1, v1 = direction, tile["sides"][direction]
        for s2, v2 in other_sides.items():
            if v1 == v2:
                ## Matched right tile
                orient2 = pairs[s1]
                sides = neighbor["sides"]
                if s2 != orient2:
                    breakout = False
                    for i in range(4):
                        neighbor = detect_sides(rotate_tile(neighbor))
                        sides = neighbor["sides"]
                        if sides[orient2] == v1:
                            tile[s1] = neighbor["name"]
                            tile_dict[neighbor["name"]] = neighbor
                            breakout = True
                            break
                    if breakout:
                        break
                    neighbor = detect_sides(flip_tile(neighbor))
                    for i in range(4):
                        neighbor = detect_sides(rotate_tile(neighbor))
                        sides = neighbor["sides"]
                        if sides[orient2] == v1:
                            tile[s1] = neighbor["name"]
                            tile_dict[neighbor["name"]] = neighbor
                            break
                else:
                    tile[s1] = neighbor["name"]
    neighbor = tile_dict[tile[direction]]
    if direction == "E":
        if not np.all(tile["img"][:, -1] == neighbor["img"][:, 0]):
            neighbor = flip_tile(neighbor, "vertical")
            tile_dict[neighbor["name"]] = neighbor
            assert np.all(tile["img"][:, -1] == neighbor["img"][:, 0]), "bad rotation"
    if direction == "S":
        if not np.all(tile["img"][-1, :] == neighbor["img"][0, :]):
            neighbor = flip_tile(neighbor, "horizontal")
            assert np.all(tile["img"][-1, :] == neighbor["img"][0, :]), "bad rotation"

    tile["visited"] = True
    return tile


def find_neighbors(tile, tile_dict):
    # def build_image(corner, tile_dict):
    # tile = deepcopy(tile_dict[corner])
    for neighbor in tile["neighbors"]:
        sides = tile["sides"]
        neighbor = tile_dict[neighbor]
        other_sides = neighbor["sides"]
        for s1, v1 in sides.items():
            for s2, v2 in other_sides.items():
                if v1 == v2:
                    orient2 = pairs[s1]
                    sides = neighbor["sides"]
                    if s2 != orient2:
                        breakout = False
                        for i in range(4):
                            neighbor = rotate_tile(neighbor)
                            sides = neighbor["sides"]
                            if sides[orient2] == v1:
                                tile[s1] = neighbor["name"]
                                tile_dict[neighbor["name"]] = neighbor
                                breakout = True
                                break
                        if breakout:
                            break
                        neighbor = flip_tile(neighbor)
                        for i in range(4):
                            neighbor = rotate_tile(neighbor)
                            sides = neighbor["sides"]
                            if sides[orient2] == v1:
                                tile[s1] = neighbor["name"]
                                tile_dict[neighbor["name"]] = neighbor
                                break
                    else:
                        tile[s1] = neighbor["name"]
    tile["visited"] = True
    return tile


def connect_tiles(tile, tile_dict):
    # tile = tile_dict[starting_id]
    tile = detect_sides(tile)
    starting_id = tile["name"]
    for i in range(12):
        # if tile['name'] == '1291':
        #     breakpoint()
        for j in range(11):
            try:
                neighbor = find_neighbor_in_dir(tile, tile_dict, "E")["E"]
            except KeyError:
                if j == 0:
                    tile = flip_tile(tile, "horizontal")
                    tile_dict[tile["name"]] = tile
                    neighbor = find_neighbor_in_dir(tile, tile_dict, "E")["E"]
            tile = tile_dict[neighbor]
        tile = tile_dict[starting_id]
        for _ in range(i + 1):
            try:
                tile = tile_dict[find_neighbor_in_dir(tile, tile_dict, "S")["S"]]
            except KeyError:
                print("are we done?")
    # tile = find_neighbors(tile, tile_dict)
    # for n in tile['neighbors']:
    #     neigh = tile_dict[n]
    #     print(neigh['name'], neigh.get('visited'))
    #     if not neigh.get('visited', False):
    #         connect_tiles(neigh, tile_dict)
    # return tile


def remove_border(tile_dict):
    for v in tile_dict.values():
        v["img"] = v["img"][1:-1, 1:-1]


def get_row(name, tile_dict, direction="E"):
    imgs = []
    tile = tile_dict[name]
    imgs.append(tile["img"])
    while direction in tile.keys():
        name = tile[direction]
        tile = tile_dict[name]
        imgs.append(tile["img"])
    return np.concatenate(imgs, axis=1)


def get_rows(name, tile_dict, direction="S"):
    imgs = []
    tile = tile_dict[name]
    imgs.append(get_row(name, tile_dict))
    print(tile["name"])
    while direction in tile.keys():
        name = tile[direction]
        tile = tile_dict[name]
        print(tile["name"])

        imgs.append(get_row(name, tile_dict))
    return np.concatenate(imgs, axis=0)


def stitch_images(starting_id, tile_dict):
    return get_rows(starting_id, tile_dict)


def build_image(starting_id, tile_dict):
    tile = tile_dict[starting_id]
    all_tiles = connect_tiles(tile, tile_dict)
    remove_border(tile_dict)
    stich_images(starting_id, tile_dict)


def show_neighbor(tile, tile_dict, direction):
    return tile_dict[tile[direction]]


if __name__ == "__main__":
    tiles = [parse_tile(tile) for tile in get_data(day=20).split("\n\n")]

    side_dict = dict()
    tile_dict = {tile["name"]: tile for tile in tiles}

    [match_sides(tile, side_dict) for tile in tiles]

    invert_dict(side_dict, tile_dict)
    print([len(tile["neighbors"]) for tile in tile_dict.values()])
    print([tile["name"] for tile in tile_dict.values() if len(tile["neighbors"]) == 2])

    corners = [
        tile["name"] for tile in tile_dict.values() if len(tile["neighbors"]) == 2
    ]

    answer_a = math.prod(map(int, corners))
    first_corner = corners[0]
    tile = tile_dict[first_corner]
    starting_id = first_corner

    tile = tile_dict[starting_id]
    all_tiles = connect_tiles(tile, tile_dict)
    remove_border(tile_dict)
    rows = stitch_images(starting_id, tile_dict)

    monster = (
        """                  # \n#    ##    ##    ###\n #  #  #  #  #  #   """.replace(
            " ", "0"
        )
        .replace("#", "1")
        .split("\n")
    )
    monster = np.concatenate(
        [np.array([int(x) for x in line]) for line in monster]
    ).reshape(3, -1)
    print()
    print(monster)

    n_monsters = max(
        (ndimage.convolve(rows, monster) == 15).sum(),
        (ndimage.convolve(rows, monster[::-1, ::-1]) == 15).sum(),
        (ndimage.convolve(rows, monster[::-1, ::]) == 15).sum(),
        (ndimage.convolve(rows, monster[::, ::-1]) == 15).sum(),
    )

    answer_b = rows.sum() - (n_monsters * monster.sum())
    submit(answer_b, day=20, year=2020)
