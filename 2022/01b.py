import fileinput


def update_top3(top3, new):
    """Try to add a new number to the top3 list.
    The 3 greatest numbers are kept.
    >>> t=[0, 0, 0]
    >>> update_top3(t, 1)
    >>> t
    [0, 0, 1]
    >>> update_top3(t, 2)
    >>> t
    [0, 1, 2]
    >>> update_top3(t, 3)
    >>> t
    [1, 2, 3]
    >>> update_top3(t, 3)
    >>> t
    [2, 3, 3]
    >>> update_top3(t, 1)
    >>> t
    [2, 3, 3]
    """
    top3.append(new)
    top3.sort()
    del top3[0]


def main():
    """read lines from the standard input
    each line is a calorie count or a separator"""
    top3 = [0, 0, 0]
    elf_calories = 0
    for line in fileinput.input():
        if not line.isspace():
            calories = int(line)
            elf_calories += calories
        else:
            update_top3(top3, elf_calories)
            elf_calories = 0
    update_top3(top3, elf_calories)
    print(top3)
    print(sum(top3))


if __name__ == "__main__":
    main()
