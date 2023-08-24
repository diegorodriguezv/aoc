import fileinput


def main():
    _map, instructions = get_map_and_instructions()
    position, facing = walk(_map, start_point(_map), parse_instructions(instructions))
    print(position, facing)
    row, col = position
    print(1000 * (row + 1) + 4 * (col + 1) + facing)


def start_point(_map):
    first_row = _map[0]
    first_col = first_row.index(".")
    return 0, first_col


def walk(_map, position, instructions):
    facing = 0
    for instruction in instructions:
        if type(instruction) is int:
            position = walk_straight(_map, position, facing, instruction)
        else:
            facing = change_facing(facing, instruction)
    return position, facing


def walk_straight(_map, position, facing, steps):
    for step in range(steps):
        position = walk_step(_map, position, facing)
    return position


def add_tuples(t1, t2):
    return tuple(map(sum, zip(t1, t2)))


def walk_step(_map, position, facing):
    new_position = add_tuples(position, facing_direction(facing))
    if not is_in_map(_map, new_position) or tile(_map, new_position) == " ":
        new_position = wrap_around(_map, position, facing)
    if tile(_map, new_position) == ".":
        return new_position
    if tile(_map, new_position) == "#":
        return position


def tile(_map, position):
    row, col = position
    return _map[row][col]


def wrap_around(_map, position, facing):
    opposite = opposite_direction(facing)
    prev = position
    while True:
        position = add_tuples(position, opposite)
        if not is_in_map(_map, position) or tile(_map, position) == " ":
            return prev
        prev = position


def is_in_map(_map, position):
    row, col = position
    return row >= 0 and row < len(_map) and col >= 0 and col < len(_map[row])


def parse_instructions(instructions):
    parts = []
    prev = 0
    curr = 0
    while curr < len(instructions):
        if instructions[curr].isalpha():
            parts.append(int(instructions[prev:curr]))
            parts.append(instructions[curr : curr + 1])
            prev = curr + 1
        curr += 1
    parts.append(int(instructions[prev:]))
    return parts


def change_facing(facing, turn):
    if turn == "R":
        return (facing + 1) % 4
    if turn == "L":
        return (facing - 1) % 4


def opposite_direction(facing):
    return facing_direction((facing + 2) % 4)


def facing_direction(facing):
    if facing == 0:
        return 0, 1
    if facing == 1:
        return 1, 0
    if facing == 2:
        return 0, -1
    if facing == 3:
        return -1, 0


def get_map_and_instructions():
    _map = []
    instructions = None
    map_finished = False
    for line in fileinput.input():
        line = line[:-1]
        if not line:
            map_finished = True
            continue
        if map_finished:
            instructions = line
        else:
            _map.append(line)
    return _map, instructions


if __name__ == "__main__":
    main()
