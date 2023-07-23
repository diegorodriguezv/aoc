import fileinput
from pprint import pp
from itertools import chain


def main():
    _map = []
    for line in fileinput.input():
        _map.append(list(map(int, line.strip())))
    fl = from_left(_map)
    print("from left")
    pp(fl)
    ft = from_top(_map)
    print("from top")
    pp(ft)
    fr = from_right(_map)
    print("from right")
    pp(fr)
    fb = from_bottom(_map)
    print("from bottom")
    pp(fb)
    print("flattened")
    flat = zip(chain(*fl), chain(*ft), chain(*fr), chain(*fb))
    print(sum([any(els) for els in flat]))


def create_vis_map(rows, cols):
    _map = []
    for _ in range(rows):
        _map.append([True] * cols)
    return _map


def from_left(_map):
    rows = len(_map)
    cols = len(_map[0])
    _max = [_map[row][0] for row in range(rows)]
    vis = create_vis_map(rows, cols)
    for col in range(1, cols - 1):
        for row in range(1, rows - 1):
            el = _map[row][col]
            if el <= _max[row]:
                vis[row][col] = False
            if el > _max[row]:
                _max[row] = el
    return vis


def from_top(_map):
    rows = len(_map)
    cols = len(_map[0])
    _max = [_map[0][col] for col in range(cols)]
    vis = create_vis_map(rows, cols)
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            el = _map[row][col]
            if el <= _max[col]:
                vis[row][col] = False
            if el > _max[col]:
                _max[col] = el
    return vis


def from_right(_map):
    rows = len(_map)
    cols = len(_map[0])
    _max = [_map[row][cols - 1] for row in range(rows)]
    vis = create_vis_map(rows, cols)
    for col in range(cols - 2, 0, -1):
        for row in range(rows - 2, 0, -1):
            el = _map[row][col]
            if el <= _max[row]:
                vis[row][col] = False
            if el > _max[row]:
                _max[row] = el
    return vis


def from_bottom(_map):
    rows = len(_map)
    cols = len(_map[0])
    _max = [_map[rows - 1][col] for col in range(cols)]
    vis = create_vis_map(rows, cols)
    for row in range(rows - 2, 0, -1):
        for col in range(cols - 2, 0, -1):
            el = _map[row][col]
            if el <= _max[col]:
                vis[row][col] = False
            if el > _max[col]:
                _max[col] = el
    return vis


if __name__ == "__main__":
    main()
