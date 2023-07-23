import fileinput


def display(xreg):
    for i, sprite in enumerate(xreg):
        col = i % 40
        if col == 0:
            print()
        if i % (40 * 6) == 0:
            print()
        if sprite - 1 <= col <= sprite + 1:
            print("#", end="")
        else:
            print(" ", end="")


def main():
    xreg = [1]
    for line in fileinput.input():
        line = line.strip()
        if line == "noop":
            xreg.append(xreg[-1])
        elif line.startswith("addx"):
            _, num = line.split()
            xreg.append(xreg[-1])
            xreg.append(xreg[-1] + int(num))
    display(xreg)


if __name__ == "__main__":
    main()
