import fileinput


def main():
    shape = get_shape()
    area = surface_area(shape)
    print(f"{area=}")


def get_faces():
    return [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ]


def get_adyacent_cube(cube, face):
    return tuple(map(sum, zip(cube, face)))


def surface_area(shape):
    exposed = 0
    faces = get_faces()
    for cube in shape:
        for face in faces:
            if get_adyacent_cube(cube, face) not in shape:
                exposed += 1
    return exposed


def get_shape():
    cubes = set()
    for line in fileinput.input():
        strings = line.strip().split(",")
        cube = tuple(map(int, strings))
        cubes.add(cube)
    return cubes


if __name__ == "__main__":
    main()
