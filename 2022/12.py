import fileinput
from collections import deque
from queue import PriorityQueue


def main():
    _map = []
    for line in fileinput.input():
        _map.append(line.strip())
    steps = a_star(_map)
    print(steps)
    print(len(steps) - 1)


def display_path(_map, steps, q):
    new_map = [list(line) for line in _map]
    for row, col in steps:
        new_map[row][col] = "."
    for line in new_map:
        print("".join(line))
    print(q.qsize())


def possible(_map, pos):
    row, col = pos
    res = []
    dirs = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    for _dir in dirs:
        row, col = _dir
        if row >= 0 and row < len(_map) and col >= 0 and col < len(_map[0]):
            new = (row, col)
            if can_move(pos_level(_map, pos), pos_level(_map, new)):
                res.append(new)
    return res


def distance(p1, p2):
    """
    >>> distance((0,0),(2,2))
    28
    >>> distance((2,2),(0,0))
    28
    >>> distance((0,0),(2,4))
    48
    >>> distance((2,4),(0,0))
    48
    >>> distance((0,0),(4,1))
    44
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    diag = min(dx, dy)
    long = max(dx, dy)
    return diag * 14 + (long - diag) * 10


def path(came_from, pos):
    path = deque()
    path.append(pos)
    while pos in came_from:
        pos = came_from[pos]
        path.appendleft(pos)
    return path


def a_star(_map):
    start = find_letter(_map, "S")
    end = find_letter(_map, "E")
    came_from = {}
    g = {}
    q = PriorityQueue()
    cost = distance(start, end)
    g[start] = 0
    q.put((cost, start))
    while not q.empty():
        _, pos = q.get()
        pos_path = path(came_from, pos)
        display_path(_map, pos_path, q)
        print()
        if pos == end:
            return pos_path
        for move in possible(_map, pos):
            new_g = g[pos] + distance(pos, move)
            if move not in g or new_g < g[move]:
                came_from[move] = pos
                g[move] = new_g
                cost = new_g + distance(move, end)
                q.put((cost, move))


def pos_level(_map, pos):
    row, col = pos
    char = _map[row][col]
    if char == "S":
        return "a"
    if char == "E":
        return "z"
    return char


def can_move(from_level, to_level):
    """True if can move from level to level.
    >>> can_move('m', 'n')
    True
    >>> can_move('m', 'o')
    False
    >>> can_move('c', 'a')
    True
    """
    return ord(to_level) - ord(from_level) <= 1


def find_letter(_map, letter):
    for row, line in enumerate(_map):
        col = line.find(letter)
        if col == -1:
            continue
        else:
            return (row, col)


if __name__ == "__main__":
    main()
