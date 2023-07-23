import fileinput


def main():
    count = 0
    for line in fileinput.input():
        first, second = line.split(",")
        first = first.split("-")
        first = tuple(map(int, first))
        second = second.split("-")
        second = tuple(map(int, second))
        if contains(first, second):
            count += 1
    print(count)


def contains(one, other):
    """
    >>> contains((2,4),(6,8))
    False
    >>> contains((2,8),(3,7))
    True
    >>> contains((6,6),(4,6))
    True
    """
    s1, e1 = one
    s2, e2 = other
    return s1 >= s2 and e1 <= e2 or s1 <= s2 and e1 >= e2


if __name__ == "__main__":
    main()
