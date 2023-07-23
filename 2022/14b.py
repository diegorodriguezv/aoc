import fileinput
from itertools import chain


def main():
    hlines = {}
    vlines = {}
    minx = miny = maxx = maxy = None
    paths = []
    for line in fileinput.input():
        path = line.strip().split(" -> ")
        paths.append([tuple(map(int, p.split(","))) for p in path])
    print(simulate(paths, (500, 0)))


def simulate(paths, source):
    _map = Map(paths, source)
    _map.print_map()
    sand = 0
    while comes_to_rest(_map):
        sand += 1
        #         print(sand)
        #         _map.print_map()
        if _map.get(source) == "o":
            break
    #         input()
    return sand


def comes_to_rest(_map):
    prev = sand = _map.source
    while True:
        sand = move(sand, _map)
        if sand is None:
            return False
        if sand == prev:
            _map.put(sand, "o")
            return True
        prev = sand


def move(sand, _map):
    sx, sy = sand
    down = (sx, sy + 1)
    if sy > _map.maxy or sx < _map.minx or sx > _map.maxx:
        return None
    if _map.get(down) == ".":
        return down
    downleft = (sx - 1, sy + 1)
    if _map.get(downleft) == ".":
        return downleft
    downright = (sx + 1, sy + 1)
    if _map.get(downright) == ".":
        return downright
    return sand


class Map:
    def __init__(self, paths, source):
        self.paths = paths
        self.source = source
        self._init_map()

    def print_map(self):
        for row in self._map:
            print("".join(row))

    def _init_map(self):
        all_points = list(chain(*self.paths)) + [self.source]
        self.maxy = max(all_points, key=lambda p: p[1])[1] + 2
        self.minx = self.source[0] - 2 * self.maxy
        self.maxx = self.source[0] + 2 * self.maxy
        #         self.minx = min(all_points, key=lambda p: p[0])[0]
        #         self.maxx = max(all_points, key=lambda p: p[0])[0]
        self.miny = min(all_points, key=lambda p: p[1])[1]
        row = ["."] * (self.maxx - self.minx + 1)
        self._map = [row.copy() for col in range(self.maxy - self.miny + 1)]
        self.put(self.source, "+")
        for path in self.paths:
            self._draw_path(path)
        self._draw_path([(self.minx, self.maxy), (self.maxx, self.maxy)])

    def _draw_path(self, path):
        prev = None
        for curr in path:
            if prev is not None:
                px, py = prev
                cx, cy = curr
                if cx == px:
                    miny = min(py, cy)
                    maxy = max(py, cy)
                    for y in range(miny, maxy + 1):
                        self.put((cx, y), "#")
                if cy == py:
                    minx = min(px, cx)
                    maxx = max(px, cx)
                    for x in range(minx, maxx + 1):
                        self.put((x, cy), "#")
            prev = curr

    def _translate(self, pos):
        x, y = pos
        newx = x - self.minx
        newy = y - self.miny
        return newx, newy

    def get(self, pos):
        x, y = self._translate(pos)
        return self._map[y][x]

    def put(self, pos, block):
        x, y = self._translate(pos)
        self._map[y][x] = block


if __name__ == "__main__":
    main()
