import fileinput
import logging


class Monkey:
    monkeys = []

    def __init__(self):
        self.name = None
        self.items = None
        self.op = None
        self.div = None
        self.ift = None
        self.iff = None
        self.inspected = 0

    def __repr__(self):
        return f"Monkey {self.name}: {self.items=} {self.op=} {self.div=} {self.ift=} {self.iff=}"

    def inspect(self):
        logging.debug(f"Monkey {self.name}:")
        for item in self.items:
            self.inspected += 1
            logging.debug(f"  Monkey inspects an item with a worry level of {item}.")
            old = item
            new = eval(self.op)
            logging.debug(f"    Worry level is {self.op} to {new}.")
            new = int(new / 3)
            logging.debug(
                f"    Monkey gets bored with item. Worry level is divided by 3 to {new}."
            )
            if new % self.div == 0:
                logging.debug(f"    Current worry level is divisible by {self.div}.")
                logging.debug(
                    f"    Item with worry level {new} is thrown to monkey {self.ift}."
                )
                self.throw(new, self.ift)
            else:
                logging.debug(
                    f"    Current worry level is not divisible by {self.div}."
                )
                logging.debug(
                    f"    Item with worry level {new} is thrown to monkey {self.iff}."
                )
                self.throw(new, self.iff)
        self.items = []

    def throw(self, item, monkey):
        self.monkeys[monkey].items.append(item)


def main():
    logging.basicConfig(filename="11.out", level=logging.DEBUG)
    monkeys = []
    monkey = None
    for line in fileinput.input():
        if line.startswith("Monkey "):
            monkey = Monkey()
            monkey.name = len(monkeys)
        elif line.startswith("  Starting items: "):
            _, items = line.split(":")
            items = items.split(", ")
            items = list(map(int, items))
            monkey.items = items
        elif line.startswith("  Operation: "):
            _, op = line.split("= ")
            monkey.op = op.strip()
        elif line.startswith("  Test: "):
            _, div = line.split("by ")
            div = int(div)
            monkey.div = div
        elif line.startswith("    If true: "):
            _, ift = line.split("monkey ")
            ift = int(ift)
            monkey.ift = ift
        elif line.startswith("    If false: "):
            _, iff = line.split("monkey ")
            iff = int(iff)
            monkey.iff = iff
        elif line.isspace():
            monkeys.append(monkey)
            monkey = Monkey()
    monkeys.append(monkey)
    Monkey.monkeys = monkeys
    print(monkeys)
    for _round in range(1, 21):
        print(f"round: {_round}")
        for monkey in monkeys:
            monkey.inspect()
        for i, monkey in enumerate(monkeys):
            print(f"Monkey {i}: {monkey.items}")
    inspected = []
    for monkey in monkeys:
        print(f"Monkey {monkey.name} inspected items {monkey.inspected} times.")
        inspected.append(monkey.inspected)
    inspected.sort()
    print(inspected[-1] * inspected[-2])


if __name__ == "__main__":
    main()
