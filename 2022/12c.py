import fileinput
from collections import deque
from queue import PriorityQueue


def main():
    _map = []
    for line in fileinput.input():
        _map.append(line.strip())
    start = find_letter(_map, "E")
    dist, prev = dijkstra(_map, start)
    all_a = find_all_a(_map)
    all_a.append(find_letter(_map, "S"))
    min_length = None
    min_a = None
    for one_a in all_a:
        if min_length is None or one_a in dist and dist[one_a] < min_length:
            min_length = dist[one_a]
            min_a = one_a
    min_path = path(prev, min_a)
    print(len(all_a))
    print(len(min_path) - 1)


def path(came_from, pos):
    path = deque()
    path.append(pos)
    while pos in came_from:
        pos = came_from[pos]
        path.appendleft(pos)
    return path


def find_all_a(_map):
    all_a = []
    for row, line in enumerate(_map):
        for col, char in enumerate(line):
            if char == "a":
                all_a.append((row, col))
    return all_a


def dijkstra(_map, start):
    dist = {}
    prev = {}
    dist[start] = 0
    q = PriorityQueue()
    q.put((0, start))
    while not q.empty():
        _, pos = q.get()
        for move in possible(_map, pos):
            new_dist = dist[pos] + distance(pos, move)
            if move not in dist or new_dist < dist[move]:
                dist[move] = new_dist
                prev[move] = pos
                q.put((new_dist, move))
    return dist, prev


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
    >>> can_move('n', 'm')
    True
    >>> can_move('o', 'm')
    False
    >>> can_move('a', 'c')
    True
    """
    return ord(from_level) - ord(to_level) <= 1


def find_letter(_map, letter):
    for row, line in enumerate(_map):
        col = line.find(letter)
        if col == -1:
            continue
        else:
            return (row, col)


if __name__ == "__main__":
    main()
