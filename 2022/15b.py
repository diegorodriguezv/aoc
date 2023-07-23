import sys
import array

# TODO:
# write n zeros to position?
# traverse all sensors and discard radius
# search for not zeros
# profit...


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


def discard_positions(sensor, radius, bit_arrays, limit):
    sx, sy = sensor
    top = sy - radius
    btm = sy + radius
    for y in range(top, btm + 1):
        if not 0 <= y <= limit:
            continue
        dy = abs(sy - y)
        start = max(sx + dy - radius, 0)
        end = min(sx - dy + radius, limit)
        for bit in range(start, end + 1):
            clear_bit(bit_arrays[y], bit)


def print_arrays(arrays):
    for i, array in enumerate(arrays):
        for i32 in reversed(array):
            print(f"{i:02}", end=" ")
            print(nibbles(i32))


def find_beacon(sensors, limit):
    arrays = []
    for i in range(0, limit + 1):
        ba = make_bit_array(limit + 1, fill=1)
        arrays.append(ba)
    #     print_arrays(arrays)
    for sensor, _, d in sensors:
        discard_positions(sensor, d, arrays, limit)
        print(sensor, d)
    #         print_arrays(arrays)
    #         input()
    for y, array in enumerate(arrays):
        for i32 in array:
            if i32 != 0:
                for x in range(0, limit + 1):
                    if test_bit(array, x):
                        return x, y


def make_bit_array(bit_size, fill=0):
    int_size = bit_size >> 5  # number of 32 bit integers
    if bit_size & 31:  # if bit_size != (32 * n) add
        int_size += 1  #    a record for stragglers
    if fill == 1:
        fill_num = 4294967295  # all bits set
    else:
        fill_num = 0  # all bits cleared
    bit_array = array.array("I")  # 'I' = unsigned 32-bit integer
    bit_array.extend((fill_num,) * int_size)
    # fill only the used bits, leave the others as zero
    if fill == 1:
        excess_bits = len(bit_array) * 32 - bit_size
        ones = 32 - excess_bits
        bit_array[-1] = 2 ** (ones) - 1
    return bit_array


def clear_bits(array_name, bit_num, num):
    """Returns a bit array with num bits set to zero starting at bit_num."""
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return array_name[record]


def test_bit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return array_name[record] & mask


# clear_bit() returns an integer with the bit at 'bit_num' cleared.
def clear_bit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return array_name[record]


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


def nibbles(num):
    snum = bin(num)[2:]
    parts = []
    end = len(snum)
    while end > 0:
        parts.append(snum[max(end - 4, 0) : end].zfill(4))
        end = end - 4
    return "_".join(reversed(parts))


if __name__ == "__main__":
    main()
