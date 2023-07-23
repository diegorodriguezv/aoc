import fileinput
from collections import deque


def row(line):
    """Returns a dict with the crates for each stack in this line.
    >>> row('    [D]    ')
    {2: 'D'}
    >>> row('[N] [C]    ')
    {1: 'N', 2: 'C'}
    >>> row('[Z] [M] [P]')
    {1: 'Z', 2: 'M', 3: 'P'}
    """
    row = 0
    contents = dict()
    while line:
        row += 1
        crate = line[:4]
        line = line[4:]
        if crate.isspace():
            continue
        content = crate[1]
        if content.isnumeric():
            break
        contents[row] = content
    return contents


def fill_stacks(stacks, crates):
    for stacknum, content in crates.items():
        stack = stacks.setdefault(stacknum, deque())
        stack.appendleft(content)


def move(line, stacks):
    _, num, _, _from, _, to = line.split()
    num, _from, to = int(num), int(_from), int(to)
    for _ in range(num):
        crate = stacks[_from].pop()
        stacks[to].append(crate)


def print_top_crates(stacks):
    top = []
    for stack in sorted(stacks.keys()):
        top.append(stacks[stack].pop())
    print("".join(top))


def main():
    drawing = True
    stacks = dict()
    for line in fileinput.input():
        if not line.isspace():
            if drawing:
                crates = row(line)
                fill_stacks(stacks, crates)
            else:
                move(line, stacks)
                # print(line, stacks)
        else:
            drawing = False
    print(stacks)
    print_top_crates(stacks)


if __name__ == "__main__":
    main()
