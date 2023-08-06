import fileinput


def main():
    encrypted = get_encrypted()
    mixed = mix_file(encrypted)
    coords = get_coordinates(mixed)
    print(coords)
    print(sum(coords))


def get_coordinates(file):
    zero_index = file.index(0)
    coord1 = (zero_index + 1000) % len(file)
    coord2 = (zero_index + 2000) % len(file)
    coord3 = (zero_index + 3000) % len(file)
    return file[coord1], file[coord2], file[coord3]


def mix_file(file, times=1):
    order = list(range(len(file)))
    for _ in range(times):
        for initial_index in range(len(file)):
            current_index = order.index(initial_index)
            number = file[initial_index]
            order = move(order, current_index, number)
    return change_order(file, order)


def change_order(file, order):
    numbers = []
    for index in order:
        numbers.append(file[index])
    return numbers


def move(order, index, positions):
    """Return the new order after moving the number at index."""
    if positions % (len(order) - 1) == 0:
        return order
    new_index = (index + positions) % (len(order) - 1)
    if positions < 0:
        if new_index == 0:
            new_index = len(order) - 1
    order1 = order[:index]
    order2 = order[index + 1 :]
    new_order = order1 + order2
    new_order1 = new_order[:new_index]
    new_order2 = new_order[new_index:]
    return new_order1 + [order[index]] + new_order2


def test_move():
    length = 6
    initial = list(range(length))
    print(initial)
    for pos in range(-10, 14):
        for index in range(length):
            print(move(initial, index, pos), index, pos)


def get_encrypted():
    encrypted = []
    for line in fileinput.input():
        encrypted.append(int(line))
    return encrypted


if __name__ == "__main__":
    main()
