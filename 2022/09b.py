import fileinput


def main():
    visited = set()
    knots = [(0, 0)] * 10
    for line in fileinput.input():
        _dir, steps = line.split()
        for _ in range(int(steps)):
            knots[0] = move(_dir, knots[0])
            for knot in range(1, 10):
                knots[knot] = follow(knots[knot], knots[knot - 1])
            print(f"{knots=}")
            visited.add(knots[-1])
    print(visited)
    print(len(visited))


def move(_dir, pos):
    x, y = pos
    if _dir == "R":
        x += 1
    if _dir == "L":
        x -= 1
    if _dir == "U":
        y += 1
    if _dir == "D":
        y -= 1
    return x, y


def follow(pos, to):
    x1, y1 = pos
    x2, y2 = to
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) == 2 and abs(dy) == 0:
        x1 += dx // 2
    elif abs(dx) == 0 and abs(dy) == 2:
        y1 += dy // 2
    elif abs(dx) == 1 and abs(dy) == 2:
        x1 += dx
        y1 += dy // 2
    elif abs(dx) == 2 and abs(dy) == 1:
        x1 += dx // 2
        y1 += dy
    elif abs(dx) == 2 and abs(dy) == 2:
        x1 += dx // 2
        y1 += dy // 2
    return x1, y1


if __name__ == "__main__":
    main()
