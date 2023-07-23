import fileinput


def find_badge(sack1, sack2, sack3):
    """
    >>> find_badge('abcd','defg', 'dhij')
    'd'
    """
    s1 = set(sack1)
    s2 = set(sack2)
    s3 = set(sack3)
    return (s1 & s2 & s3).pop()


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
    count = 0
    l1 = l2 = l3 = ""
    for line in fileinput.input():
        line = line.strip()
        if count % 3 == 0:
            l1 = line
        if count % 3 == 1:
            l2 = line
        if count % 3 == 2:
            l3 = line
            sump += priority_value(find_badge(l1, l2, l3))
        count += 1
    print(sump)


if __name__ == "__main__":
    main()
