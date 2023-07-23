import sys
import array


def main():
    sensors = []
    filename = sys.argv[1]
    limit = int(sys.argv[2])
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
    position = find_beacon(sensors, limit)
    px, py = position
    print(px * 4_000_000 + py)


def update_borders(borders, new):
    for y, xset in new.items():
        if y in borders:
            borders[y].update(xset)
        else:
            borders[y] = xset


def find_beacon(sensors, limit):
    all_borders = {}
    for sensor, _, d in sensors:
        border = border_positions(sensor, d + 1, limit)
        update_borders(all_borders, border)
    for y, xset in all_borders.items():
        for x in xset:
            border = (x, y)
            if all(distance(border, sensor) > d for sensor, _, d in sensors):
                return border


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def border_positions(sensor, radius, limit):
    positions = {}
    sx, sy = sensor
    top = sy - radius
    btm = sy + radius
    for y in range(top, btm + 1):
        if not 0 <= y <= limit:
            continue
        dy = abs(sy - y)
        start = sx + dy - radius
        if start >= 0:
            positions.setdefault(y, set()).add(start)
        end = sx - dy + radius
        if end <= limit:
            positions.setdefault(y, set()).add(end)
    return positions


if __name__ == "__main__":
    main()
