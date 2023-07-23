import fileinput


def find_start(line):
    for i in range(len(line)):
        window = line[i : i + 4]
        if len(set(window)) == 4:
            return i + 4


def main():
    for line in fileinput.input():
        print(find_start(line))


if __name__ == "__main__":
    main()
