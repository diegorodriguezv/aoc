import fileinput

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1),
}
SCANS = {
    "N": ["N", "NE", "NW"],
    "S": ["S", "SE", "SW"],
    "W": ["W", "NW", "SW"],
    "E": ["E", "NE", "SE"],
}


def main():
    elves = get_elve_positions()
    directions = "NSWE"
    turn = 1
    while True:
        next_turn = one_turn(elves, directions)
        if next_turn:
            elves, directions = next_turn
        else:
            break
        turn += 1
    print("final turn", turn)


def one_turn(elves, directions):
    proposals = []
    movecount = {}
    for elf in elves:
        proposal = None
        for direction in directions:
            if all(move(elf, DIRS[scan]) not in elves for scan in SCANS[direction]):
                proposal = move(elf, DIRS[direction])
                break
        if all(move(elf, DIRS[dir]) not in elves for dir in DIRS):
            proposal = None
        if proposal in movecount:
            movecount[proposal] += 1
        else:
            movecount[proposal] = 1
        proposals.append(proposal)
    if None in movecount and movecount[None] == len(elves):
        return None
    moved_elves = set()
    for elf, proposal in zip(elves, proposals):
        if proposal and movecount[proposal] == 1:
            moved_elves.add(proposal)
        else:
            moved_elves.add(elf)
    directions = directions[1:] + directions[0]
    return moved_elves, directions


def move(elf, direction):
    return tuple(map(sum, zip(elf, direction)))


def get_rectangle(elves):
    minx = min(elf[0] for elf in elves)
    maxx = max(elf[0] for elf in elves)
    miny = min(elf[1] for elf in elves)
    maxy = max(elf[1] for elf in elves)
    return minx, maxx, miny, maxy


def rectangle_area(rectangle):
    minx, maxx, miny, maxy = rectangle
    area = (maxx - minx + 1) * (maxy - miny + 1)
    return area


def get_elve_positions():
    elves = set()
    row = 0
    for line in fileinput.input():
        start = 0
        while start < len(line):
            col = line.find("#", start)
            if col == -1:
                break
            elves.add((row, col))
            start = col + 1
        row += 1
    return elves


if __name__ == "__main__":
    main()
