import fileinput
from pprint import pp
from itertools import chain, starmap

WIDTH = 80


def main():
    _map = []
    for line in fileinput.input():
        _map.append(list(map(int, line.strip())))
    fl = from_left(_map)
    print("from left")
    pp(fl, width=WIDTH)
    ft = from_top(_map)
    print("from top")
    pp(ft, width=WIDTH)
    fr = from_right(_map)
    print("from right")
    pp(fr, width=WIDTH)
    fb = from_bottom(_map)
    print("from bottom")
    pp(fb, width=WIDTH)
    flat = zip(chain(*fl), chain(*ft), chain(*fr), chain(*fb))
    scenic_score = starmap(lambda n1, n2, n3, n4: n1 * n2 * n3 * n4, flat)
    print("score")
    print(max(scenic_score))


def create_vis_map(rows, cols):
    _map = []
    for _ in range(rows):
        _map.append([0] * cols)
    return _map


def from_left(_map):
    rows = len(_map)
    cols = len(_map[0])
    vis = create_vis_map(rows, cols)
    for row in range(1, rows - 1):
        pos_block = [0] * 10
        for col in range(1, cols - 1):
            el = _map[row][col]
            vis[row][col] = col - pos_block[el]
            pos_block[: el + 1] = [col] * (el + 1)
    return vis


def from_top(_map):
    rows = len(_map)
    cols = len(_map[0])
    vis = create_vis_map(rows, cols)
    for col in range(1, cols - 1):
        pos_block = [0] * 10
        for row in range(1, rows - 1):
            el = _map[row][col]
            vis[row][col] = row - pos_block[el]
            pos_block[: el + 1] = [row] * (el + 1)
    return vis


def from_right(_map):
    rows = len(_map)
    cols = len(_map[0])
    vis = create_vis_map(rows, cols)
    for row in range(rows - 2, 0, -1):
        pos_block = [cols - 1] * 10
        for col in range(cols - 2, 0, -1):
            el = _map[row][col]
            vis[row][col] = pos_block[el] - col
            pos_block[: el + 1] = [col] * (el + 1)
    return vis


def from_bottom(_map):
    rows = len(_map)
    cols = len(_map[0])
    vis = create_vis_map(rows, cols)
    for col in range(cols - 2, 0, -1):
        pos_block = [rows - 1] * 10
        for row in range(rows - 2, 0, -1):
            el = _map[row][col]
            vis[row][col] = pos_block[el] - row
            pos_block[: el + 1] = [row] * (el + 1)
    return vis


if __name__ == "__main__":
    main()
