import sys


def main():
    sensors = []
    filename = sys.argv[1]
    yline = int(sys.argv[2])
    with open(filename) as f:
        for line in f.readlines():
            [sensor, beacon] = line.strip().split(":")
            _, _, sensor = sensor.partition("at ")
            sensorx, _, sensory = sensor.partition(", ")
            _, _, sensorx = sensorx.partition("=")
            _, _, sensory = sensory.partition("=")
            _, _, beacon = beacon.partition("at ")
            beaconx, _, beacony = beacon.partition(", ")
            _, _, beaconx = beaconx.partition("=")
            _, _, beacony = beacony.partition("=")
            sensor = (int(sensorx), int(sensory))
            beacon = (int(beaconx), int(beacony))
            sensors.append((sensor, beacon, distance(sensor, beacon)))
    positions = beacon_not_present(sensors, yline)
    print(len(positions))


def beacon_not_present(sensors, yline):
    positions = set()
    for sensor, _, d in sensors:
        xrange = yintersections(sensor, d, yline)
        if not xrange:
            continue
        x1, x2 = xrange
        for x in range(x1, x2 + 1):
            positions.add(x)
    for _, beacon, _ in sensors:
        bx, by = beacon
        if by == yline:
            positions.discard(bx)
    return positions


def yintersections(sensor, d, yline):
    """Returns a range of the x positions along the y coordinate (yline) that lie
    within distance d of a given sensor coordinates or None.
    >>> yintersections((8,7),9,-3)
    >>> yintersections((8,7),9,-2)
    (8, 8)
    >>> yintersections((8,7),9,-1)
    (7, 9)
    >>> yintersections((8,7),9,7)
    (-1, 17)
    """
    sx, sy = sensor
    ydiff = abs(yline - sy)
    if ydiff > d:
        return None
    return (sx + ydiff - d, sx - ydiff + d)


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    main()
