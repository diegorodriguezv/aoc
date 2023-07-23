import fileinput


def main():
    count = 0
    for line in fileinput.input():
        first, second = line.split(",")
        first = first.split("-")
        first = tuple(map(int, first))
        second = second.split("-")
        second = tuple(map(int, second))
        if overlaps(first, second):
            count += 1
    print(count)


def overlaps(one, other):
    """
    >>> overlaps((2,3),(4,5))
    False
    >>> overlaps((5,7),(7,9))
    True
    >>> overlaps((2,6),(4,8))
    True

       s1   e1
    s2   e2
           s2  e2
    s2         e2
    """
    s1, e1 = one
    s2, e2 = other
    return not (e2 < s1 or s2 > e1) and not (e1 < s2 or s1 > e2)


if __name__ == "__main__":
    main()
