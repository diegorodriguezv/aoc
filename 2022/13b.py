import fileinput
from pprint import pp


def main():
    packets = []
    for line in fileinput.input():
        if not line.isspace():
            packets.append(eval(line))
    sep1 = [[2]]
    sep2 = [[6]]
    packets.extend([sep1, sep2])
    pp(packets)
    packets.sort(key=isinorderkey())
    pp(packets)
    idx1 = packets.index(sep1) + 1
    idx2 = packets.index(sep2) + 1
    print(idx1, idx2, idx1 * idx2)


def isinorderkey():
    class K:
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return isinorder(self.obj, other.obj)

    return K


def isinorder(p1, p2, level=0):
    for left, right in zip(p1, p2):
        if type(left) is int and type(right) is int:
            if left > right:
                return False
            elif left < right:
                return True
        elif type(left) is list and type(right) is list:
            comp = isinorder(left, right, level + 1)
            if not comp is None:
                return comp
        elif type(left) is int and type(right) is list:
            comp = isinorder([left], right, level + 1)
            if not comp is None:
                return comp
        elif type(left) is list and type(right) is int:
            comp = isinorder(left, [right], level + 1)
            if not comp is None:
                return comp
        else:
            raise TypeError(f"Invalid types: {left=} {right=}")
    if len(p1) < len(p2):
        return True
    elif len(p1) > len(p2):
        return False
    else:
        return None


if __name__ == "__main__":
    main()
