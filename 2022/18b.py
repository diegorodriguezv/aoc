import fileinput


def main():
    shape = get_shape()
    area = surface_area(shape)
    print(f"{area=}")
    exterior_area = exterior_faces(shape)
    print(f"{len(exterior_area)=}")


def exterior_faces(shape):
    names = get_faces_by_name()
    neighbors = get_face_connections()
    cube = min(shape)
    stack = [(cube, names["x-"])]
    # visited = set()
    visited = list()
    while stack:
        cube, face = stack.pop()
        if (cube, face) not in visited:
            assert get_adjacent_cube(cube, face) not in shape
            # visited.add((cube, face))
            visited.append((cube, face))
            for neighbor in neighbors[face]:
                adjacent_cube = get_adjacent_cube(cube, neighbor)
                cube_adjacent_to_adjacent_cube = get_adjacent_cube(adjacent_cube, face)
                if cube_adjacent_to_adjacent_cube in shape:
                    opposite = opposite_face(neighbor)
                    stack.append((cube_adjacent_to_adjacent_cube, opposite))
                elif adjacent_cube in shape:
                    stack.append((adjacent_cube, face))
                else:
                    stack.append((cube, neighbor))
    return visited


def exterior_surface_area(shape):
    names = get_faces_by_name()
    neighbors = get_face_connections()
    cube = min(shape)
    stack = [(cube, names["x-"])]
    visited = set()
    while stack:
        cube, face = stack.pop()
        if (cube, face) not in visited:
            assert get_adjacent_cube(cube, face) not in shape
            visited.add((cube, face))
            for neighbor in neighbors[face]:
                adjacent_cube = get_adjacent_cube(cube, neighbor)
                if adjacent_cube in shape:
                    cube_adjacent_to_adjacent_cube = get_adjacent_cube(
                        adjacent_cube, face
                    )
                    if cube_adjacent_to_adjacent_cube in shape:
                        opposite = opposite_face(neighbor)
                        stack.append((cube_adjacent_to_adjacent_cube, opposite))
                    else:
                        stack.append((adjacent_cube, face))
                else:
                    stack.append((cube, neighbor))
    return len(visited)


def opposite_face(face):
    return tuple(-coord for coord in face)


def get_face_connections():
    faces = get_faces_by_name()
    return {
        faces["x+"]: [faces["y+"], faces["y-"], faces["z+"], faces["z-"]],
        faces["y+"]: [faces["x+"], faces["x-"], faces["z+"], faces["z-"]],
        faces["z+"]: [faces["y+"], faces["y-"], faces["x+"], faces["x-"]],
        faces["x-"]: [faces["y+"], faces["y-"], faces["z+"], faces["z-"]],
        faces["y-"]: [faces["x+"], faces["x-"], faces["z+"], faces["z-"]],
        faces["z-"]: [faces["y+"], faces["y-"], faces["x+"], faces["x-"]],
    }


def get_names_by_face():
    return {face: name for name, face in get_faces_by_name().items()}


def get_faces_by_name():
    faces = get_faces()
    return {
        "x+": faces[0],
        "y+": faces[1],
        "z+": faces[2],
        "x-": faces[3],
        "y-": faces[4],
        "z-": faces[5],
    }


def get_faces():
    return [
        (1, 0, 0),  # x+
        (0, 1, 0),  # y+
        (0, 0, 1),  # z+
        (-1, 0, 0),  # x-
        (0, -1, 0),  # y-
        (0, 0, -1),  # z-
    ]


def get_adjacent_cube(cube, face):
    return tuple(map(sum, zip(cube, face)))


def surface_area(shape):
    exposed = 0
    faces = get_faces()
    for cube in shape:
        for face in faces:
            if get_adjacent_cube(cube, face) not in shape:
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
