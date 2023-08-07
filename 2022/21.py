import fileinput


def main():
    monkeys = get_monkeys()
    print(get_value(monkeys, "root"))


def get_value(monkeys, monkey):
    data = monkeys[monkey]
    if len(data) == 1:
        return int(data[0])
    value1 = get_value(monkeys, data[0])
    op = data[1]
    value2 = get_value(monkeys, data[2])
    if op == "+":
        return value1 + value2
    if op == "*":
        return value1 * value2
    if op == "/":
        return value1 / value2
    if op == "-":
        return value1 - value2


def get_monkeys():
    monkeys = {}
    for line in fileinput.input():
        node, _, data = line.strip().partition(": ")
        data = data.split()
        monkeys[node] = data
    return monkeys


if __name__ == "__main__":
    main()
