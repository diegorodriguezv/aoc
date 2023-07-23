import fileinput


def find_common_item(sack1, sack2):
    """
    >>> find_common_item('abcd','defg')
    'd'
    """
    s1 = set(sack1)
    s2 = set(sack2)
    return s1.intersection(s2).pop()


def priority_value(char):
    """Calculate the priority of an item type.
    >>> priority_value('p')
    16
    >>> priority_value('L')
    38
    >>> priority_value('P')
    42
    >>> priority_value('v')
    22
    """
    if char.islower():
        return ord(char) - ord("a") + 1
    if char.isupper():
        return ord(char) - ord("A") + 27


def main():
    sump = 0
    for line in fileinput.input():
        line = line.strip()
        l = len(line)
        s1 = line[: l // 2]
        s2 = line[l // 2 :]
        sump += priority_value(find_common_item(s1, s2))
    print(sump)


if __name__ == "__main__":
    main()
