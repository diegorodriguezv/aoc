import fileinput


def main():
    """read lines from the standard input
    each line is a calorie count or a separator"""
    elf = 1
    max_calories = 0
    elf_calories = 0
    for line in fileinput.input():
        if not line.isspace():
            calories = int(line)
            elf_calories += calories
        else:
            if elf_calories > max_calories:
                max_calories = elf_calories
            elf_calories = 0
    if elf_calories > max_calories:
        max_calories = elf_calories
    print(max_calories)


if __name__ == "__main__":
    main()
