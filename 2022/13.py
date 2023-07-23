import fileinput
import logging


def main():
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    index = which = 1
    inorder = []
    first = second = None
    for line in fileinput.input():
        if which == 1:
            which = 2
            first = line.strip()
        elif which == 2:
            which = 3
            second = line.strip()
            logging.debug(f"== Pair {index} ==")
            logging.debug(f"- Compare {first} vs {second}")
            if isinorder(eval(first), eval(second)):
                inorder.append(index)
            index += 1
        elif which == 3:
            which = 1
            assert line.isspace()
        else:
            raise ValueError()
    print(inorder)
    print(sum(inorder))


def isinorder(p1, p2, level=0):
    for left, right in zip(p1, p2):
        if type(left) is int and type(right) is int:
            logging.debug("  " * level + f"  - Compare {left} vs {right}")
            if left > right:
                logging.debug(
                    "  " * (level + 1)
                    + f"  - Right side is smaller, so inputs are not in the right order"
                )
                return False
            elif left < right:
                logging.debug(
                    "  " * (level + 1)
                    + f"  - Left side is smaller, so inputs are in the right order"
                )
                return True
        elif type(left) is list and type(right) is list:
            logging.debug("  " * level + f"  - Compare {left} vs {right}")
            comp = isinorder(left, right, level + 1)
            if not comp is None:
                return comp
        elif type(left) is int and type(right) is list:
            logging.debug("  " * level + f"  - Compare {left} vs {right}")
            logging.debug(
                "  " * (level + 1)
                + f"  - Mixed types; convert left to [{left}] and retry comparison"
            )
            comp = isinorder([left], right, level + 1)
            if not comp is None:
                return comp
        elif type(left) is list and type(right) is int:
            logging.debug("  " * level + f"  - Compare {left} vs {right}")
            logging.debug(
                "  " * (level + 1)
                + f"  - Mixed types; convert right to [{right}] and retry comparison"
            )
            comp = isinorder(left, [right], level + 1)
            if not comp is None:
                return comp
        else:
            raise TypeError(f"Invalid types: {left=} {right=}")
    if len(p1) < len(p2):
        logging.debug(
            "  " * (level + 1)
            + f"  - Left side ran out of items, so inputs are in the right order"
        )
        return True
    elif len(p1) > len(p2):
        logging.debug(
            "  " * (level + 1)
            + f"  - Right side ran out of items, so inputs are not in the right order"
        )
        return False
    else:
        return None


if __name__ == "__main__":
    main()
