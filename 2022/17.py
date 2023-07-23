import fileinput
from itertools import cycle

# TODO:
# implement collide left, right and floor
# implement collide terrain
# implement world


def main():
    moves = []
    for line in fileinput.input():
        for char in line.strip():
            if char == "<":
                moves.append(-1)
            if char == ">":
                moves.append(1)
    tower = simulate(shapes(), moves, 2022)
    print(len(tower))


def simulate(shapes, moves, rocks):
    shapegen = cycle(shapes)
    movegen = cycle(moves)
    tower = []
    for rock in range(rocks):
        #         print(f"{rock=}")
        shape = next(shapegen)
        shape_pos = locate(shape, tower)
        #         print_simulation(shape, shape_pos, tower)
        while True:
            delta_x = next(movegen)
            shape_pos = move(shape, shape_pos, tower, delta_x)
            #             print_simulation(shape, shape_pos, tower)
            new_pos = fall(shape, shape_pos, tower)
            if new_pos == shape_pos:
                tower = add_rock(shape, new_pos, tower)
                break
            shape_pos = new_pos
    #             print_simulation(shape, shape_pos, tower)
    return tower


def print_simulation(shape, shape_pos, tower):
    shape_height = len(shape)
    tower_height = len(tower)
    shape_width = len(shape[0])
    shape_height = len(shape)
    shape_x, shape_y = shape_pos
    for y in range(max(tower_height, shape_y), 0, -1):
        line = ["."] * 7
        if shape_y - shape_height < y <= shape_y:
            for x, col in enumerate(shape[shape_y - y]):
                if col:
                    line[x + shape_x] = "@"
        if y <= tower_height:
            for x, col in enumerate(tower[y - 1]):
                if col:
                    line[x] = "#"
        print("".join(line))
    print("-" * 7)


def locate(shape, tower):
    shape_height = len(shape)
    tower_height = len(tower)
    return 2, tower_height + 3 + shape_height


def collides(shape, pos, tower):
    shape_height = len(shape)
    shape_width = len(shape[0])
    tower_height = len(tower)
    pos_x, pos_y = pos
    if tower_height <= pos_y - shape_height:
        return False
    for y, row in enumerate(reversed(shape)):
        if y + pos_y - shape_height > tower_height - 1:
            return False
        for x, col in enumerate(row):
            if col and tower[y + pos_y - shape_height][x + pos_x]:
                return True
    return False


def move(shape, pos, tower, delta_x):
    shape_height = len(shape)
    shape_width = len(shape[0])
    tower_height = len(tower)
    pos_x, pos_y = pos
    new_x = pos_x + delta_x
    if (
        new_x >= 0
        and new_x + shape_width <= 7
        and not collides(shape, (new_x, pos_y), tower)
    ):
        pos_x = new_x
    return pos_x, pos_y


def fall(shape, pos, tower):
    shape_height = len(shape)
    shape_width = len(shape[0])
    tower_height = len(tower)
    pos_x, pos_y = pos
    if pos_y - shape_height > 0 and not collides(shape, (pos_x, pos_y - 1), tower):
        pos_y -= 1
    return pos_x, pos_y


def add_rock(shape, pos, tower):
    pos_x, pos_y = pos
    shape_height = len(shape)
    tower_height = len(tower)
    for y, row in enumerate(reversed(shape)):
        if pos_y - shape_height + y < tower_height:
            for x, col in enumerate(row):
                if col:
                    tower[pos_y - shape_height + y][x + pos_x] = col
        else:
            new_row = []
            new_row.extend([0] * pos_x)
            new_row.extend(row)
            new_row.extend([0] * (7 - len(new_row)))
            assert len(new_row) == 7
            tower.append(new_row)
    return tower


def shapes():
    shapes = []
    shape = [[1, 1, 1, 1]]
    shapes.append(shape)
    shape = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    shapes.append(shape)
    shape = [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
    shapes.append(shape)
    shape = [[1], [1], [1], [1]]
    shapes.append(shape)
    shape = [[1, 1], [1, 1]]
    shapes.append(shape)
    return shapes


if __name__ == "__main__":
    main()
