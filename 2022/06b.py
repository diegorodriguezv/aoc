import fileinput


def find_start(line):
    for i in range(len(line)):
        window = line[i : i + 14]
        if len(set(window)) == 14:
            return i + 14


def main():
    for line in fileinput.input():
        print(find_start(line))


if __name__ == "__main__":
    main()
