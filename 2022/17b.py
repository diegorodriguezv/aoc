from sys import argv
from pprint import pp


def progressive_simulations(rock_num, sample_size, shape_list, gas_jets):
    """Do partial simulations of sample_size until achieving total rock_num.
    Used for exploratory purposes.
    """
    tower, rock, jet = [], 0, 0
    fallen = 0
    prev_size = 0
    while fallen < rock_num:
        rocks = min(sample_size, rock_num - fallen)
        tower, rock, jet = simulate(shape_list, gas_jets, rocks, tower, rock, jet)
        new_size = len(tower)
        diff = new_size - prev_size
        print(f"{rocks=} {prev_size=} {new_size=} {diff=}")
        prev_size = new_size
        fallen += rocks
        # print_tower(tower)
    print(f"{len(tower)=}")
    found = find_tower_period(tower)
    if found:
        period, start, end = found
        print(f"{period=} {start=} {end=}")


def calculate_answer(rock_num, shape_list, gas_jets):
    """Calculate the answer without simulating the whole tower.
    First find the tower repetition period (tower period).
    Then find the number of rocks that create that period (rock period).
    Then simulate two samples of the rock period to find the first and last segments.
    Then calculate the total tower length arithmetically and print the answer.
    """
    sufficient_sample = 2000
    tower, _, _ = simulate(shape_list, gas_jets, sufficient_sample, [], 0, 0)
    found = find_tower_period(tower)
    if found:
        tower_period, start, end = found
        print(f"{tower_period=} {start=} {end=}")
    assert found, "Period not found, can't continue. Try increasing sufficient_sample."
    # Skip the first part of the tower that does not repeats
    tower, rock, jet = simulate(shape_list, gas_jets, tower_period, [], 0, 0)
    first_size = len(tower)
    # Simulate one by one until the tower grows by a tower period
    for rock_period in range(tower_period * 2):
        tower, rock, jet = simulate(shape_list, gas_jets, 1, tower, rock, jet)
        if len(tower) - first_size > tower_period:
            break
    print(f"{rock_period=}")
    # Solve the problem by dividing the simulation in partitions of rock_period
    partitions = rock_num // rock_period
    remaining = rock_num % rock_period
    # We only need to simulate the first and last partitions to find their heights
    # All other partitions are of tower_period height
    tower, rock, jet = simulate(shape_list, gas_jets, rock_period, [], 0, 0)
    first_partition_size = len(tower)
    tower, rock, jet = simulate(shape_list, gas_jets, remaining, tower, rock, jet)
    last_partition_size = len(tower) - first_partition_size
    print(f"{partitions=} {remaining=} {first_partition_size=} {last_partition_size=}")
    return first_partition_size + (partitions - 1) * tower_period + last_partition_size


def main():
    gas_jets = get_gas_jets()
    print(f"{len(gas_jets)=}")
    shape_list = get_shapes()
    rock_num = int(argv[2])
    answer = calculate_answer(rock_num, shape_list, gas_jets)
    print(f"{answer=}")


def get_gas_jets():
    gas_jets = []
    with open(argv[1]) as f:
        for line in f.readlines():
            for char in line.strip():
                if char == "<":
                    gas_jets.append(-1)
                if char == ">":
                    gas_jets.append(1)
    return gas_jets


def simulate(shapes, jets, rock_number, tower, initial_rock, initial_jet):
    """Do a simulation of rock_number rocks falling.

    :param shapes: the list of shapes that rocks can take
    :param jets: the list of jets of gas
    :param rock_number: the number of rocks that will fall in the simulation
    :param tower: the tower of rocks before the simulation starts
    :param initial_rock: the index of the first rock to fall
    :param initial_jet: the index of the first gas jet to use
    :returns: a tuple with the resulting tower, the next rock index and the next jet index
    """
    shapelen = len(shapes)
    movelen = len(jets)
    jet_index = initial_jet
    rock_index = initial_rock
    for rock in range(rock_number):
        shape = shapes[rock_index % shapelen]
        rock_index += 1
        shape_pos = spawn_rock(shape, tower)
        while True:
            delta_x = jets[jet_index % movelen]
            jet_index += 1
            shape_pos = move_rock(shape, shape_pos, tower, delta_x)
            new_pos = fall_rock(shape, shape_pos, tower)
            if new_pos == shape_pos:
                tower = add_rock_to_tower(shape, new_pos, tower)
                break
            shape_pos = new_pos
    return tower, rock_index, jet_index


def find_tower_period(tower):
    # Find repeating period in the tower of rocks from the start
    # start from the beginning looking forward for occurrences
    # when one is found increase the offset
    # when more than certain treshold occurrences are found declare a period found
    # when the repetitions stops rollback
    # return the first line to repeat also
    treshold = 100
    count = 0
    start = 0
    while start < len(tower):
        end = start + 1
        while end < len(tower):
            if tower[end] == tower[start]:
                count += 1
                if count == treshold:
                    period = end - start
                    return period, start - treshold + 1, end - treshold + 1
                start += 1
            else:
                end -= count
                start -= count
                count = 0
            end += 1
        start += 1


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


def print_tower(tower, start=0, end=-1):
    begin = None
    if end < 0:
        begin = len(tower) + end
    else:
        begin = end
    if start < 0:
        stop = len(tower) + start + 1
    else:
        stop = start
    for curr in range(begin, stop - 1, -1):
        line = []
        for pos in tower[curr]:
            if pos:
                line.append("#")
            else:
                line.append(".")
        print("".join(line), curr)


def spawn_rock(shape, tower):
    shape_height = len(shape)
    tower_height = len(tower)
    return 2, tower_height + 3 + shape_height


def rock_collides(shape, pos, tower):
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


def move_rock(shape, pos, tower, delta_x):
    shape_height = len(shape)
    shape_width = len(shape[0])
    tower_height = len(tower)
    pos_x, pos_y = pos
    new_x = pos_x + delta_x
    if (
        new_x >= 0
        and new_x + shape_width <= 7
        and not rock_collides(shape, (new_x, pos_y), tower)
    ):
        pos_x = new_x
    return pos_x, pos_y


def fall_rock(shape, pos, tower):
    shape_height = len(shape)
    shape_width = len(shape[0])
    tower_height = len(tower)
    pos_x, pos_y = pos
    if pos_y - shape_height > 0 and not rock_collides(shape, (pos_x, pos_y - 1), tower):
        pos_y -= 1
    return pos_x, pos_y


def add_rock_to_tower(shape, pos, tower):
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


def get_shapes():
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
