import fileinput


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
    print(xreg)
    res = 0
    if len(xreg) > 220:
        idxs = [20, 60, 100, 140, 180, 220]
        for idx in idxs:
            print(xreg[idx - 1])
            res += idx * xreg[idx - 1]
    print(res)


if __name__ == "__main__":
    main()
