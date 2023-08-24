import fileinput
import pprint

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
NAME = {RIGHT: "RIGHT", DOWN: "DOWN", LEFT: "LEFT", UP: "UP"}


def main():
    _map, instructions = get_map_and_instructions()
    position, facing = walk(_map, parse_instructions(instructions))
    print(position, facing)
    row, col = position
    print(1000 * (row + 1) + 4 * (col + 1) + facing)


def adjacent_corners(cube, corners, facing):
    """Find the corners for the face adjacent to corners in the given direction.
    The way to find it is: The face that shares two corners with this one but has at
    least one different corner. (It's not the original face).
    """
    e1, e2 = corners_edge(corners, facing)
    for face_corners in cube:
        if (
            e1 in face_corners
            and e2 in face_corners
            and any(corner not in corners for corner in face_corners)
        ):
            return face_corners


def corners_edge(corners, facing):
    ul, ur, dl, dr = corners
    if facing == UP:
        edge = ul, ur
    if facing == DOWN:
        edge = dl, dr
    if facing == LEFT:
        edge = ul, dl
    if facing == RIGHT:
        edge = ur, dr
    return edge


def side_facing(side):
    if side == UP or side == DOWN:
        return RIGHT
    if side == LEFT or side == RIGHT:
        return DOWN


def rotate_corners(corners, turn):
    """Rotate corners given a direction to turn."""
    ul, ur, dl, dr = corners
    if turn == "L":
        return dl, ul, dr, ur
    if turn == "R":
        return ur, dr, ul, dl


def rotated_adjacent_corners(cube, corners, facing):
    """Find the corners for the face adjacento to corners facing in a certain direction,
    but rotated so that the edge shared with the current face is located apropriately.
    """
    rotated = adjacent_corners(cube, corners, facing)
    for rotations in range(4):
        if corners_edge(corners, facing) == corners_edge(
            rotated, opposite_facing(facing)
        ):
            return rotated, rotations
        rotated = rotate_corners(rotated, "R")
        rotations += 1


def wrapped_edges(faces):
    """Assign cube corners to each face (wrap) and return the edges for faces without an adjacent face in the map.
    f----g
    | \  | \
    |   a----b
    |   ||   |
    |   ||   |
    i---|h   |
      \ |  \ |
        d----c
    faces:  
    4 1 5
      2
      3
      4
    """
    visited = set()
    edges = {}
    # corners for each face in a cube (left -> right, top -> bottom)
    cube = list(map(tuple, ["abdc", "dcih", "ihfg", "fgab", "faid", "bgch"]))
    work = [(faces[0], cube[0], 0)]
    while work:
        face, corners, rotations = work.pop()
        if face in visited:
            continue
        visited.add(face)
        for facing in [RIGHT, DOWN, LEFT, UP]:
            neighbor_face = adjacent_face(face, faces, facing)
            if neighbor_face:
                neighbor_corners, rotations = rotated_adjacent_corners(
                    cube, corners, facing
                )
                work.append((neighbor_face, neighbor_corners, rotations))
            else:
                edges[(face, facing)] = corners_edge(corners, facing)
    return edges


def start_point(_map):
    first_row = _map[0]
    first_col = first_row.index(".")
    return 0, first_col


def walk(_map, instructions):
    facing = 0
    position = start_point(_map)
    side_length = get_side_length(_map)
    seams = create_seams(_map, side_length)
    for instruction in instructions:
        if type(instruction) is int:
            position, facing = walk_straight(_map, position, facing, instruction, seams)
        else:
            facing = change_facing(facing, instruction)
    return position, facing


def walk_straight(_map, position, facing, steps, seams):
    for step in range(steps):
        position, facing = walk_step(_map, position, facing, seams)
    return position, facing


def add_tuples(t1, t2):
    return tuple(map(sum, zip(t1, t2)))


def walk_step(_map, position, facing, seams):
    new_position = add_tuples(position, facing_direction(facing))
    new_facing = facing
    if not is_in_map(_map, new_position) or tile(_map, new_position) == " ":
        new_position, new_facing = seams[position, facing]
    if tile(_map, new_position) == ".":
        return new_position, new_facing
    if tile(_map, new_position) == "#":
        return position, facing


def tile(_map, position):
    row, col = position
    return _map[row][col]


def get_side_length(_map):
    total_area = sum(1 for row in _map for char in row if char != " ")
    return int((total_area / 6) ** 0.5)


def face_map(_map, side_length):
    faces = []
    face_row = 0
    while face_row < len(_map):
        face_col = 0
        while face_col < len(_map[face_row]):
            if tile(_map, (face_row, face_col)) != " ":
                faces.append((face_row // side_length, face_col // side_length))
            face_col += side_length
        face_row += side_length
    return faces


def adjacent_face(face, faces, facing):
    adjacent_face = add_tuples(face, facing_direction(facing))
    return adjacent_face if adjacent_face in faces else None


def start_edge_coordinates(face, side, side_length, _dir):
    """Returns the start coordinates of the side edge of a map face in
    a given direction."""
    face_row, face_col = face
    top, left = face_row * side_length, face_col * side_length
    bottom, right = (face_row + 1) * side_length - 1, (face_col + 1) * side_length - 1
    if side == LEFT:
        return (top, left) if _dir != UP else (bottom, left)
    if side == UP:
        return (top, left) if _dir != LEFT else (top, right)
    if side == DOWN:
        return (bottom, left) if _dir != LEFT else (bottom, right)
    if side == RIGHT:
        return (top, right) if _dir != UP else (bottom, right)


def create_seams(_map, side_length):
    edges = wrapped_edges(face_map(_map, side_length))
    paired = set()
    seams = {}
    for (face, side), edge in edges.items():
        for (pair_face, pair_side), pair_edge in edges.items():
            if set(edge) == set(pair_edge) and pair_face != face:
                break
        if (pair_face, pair_side) in paired:
            continue
        paired.add((face, side))
        facing1 = side_facing(side)
        pos1 = start_edge_coordinates(face, side, side_length, facing1)
        dir1 = facing_direction(facing1)
        facing2 = side_facing(pair_side)
        if edge != pair_edge:
            facing2 = opposite_facing(facing2)
        pos2 = start_edge_coordinates(pair_face, pair_side, side_length, facing2)
        dir2 = facing_direction(facing2)
        print(NAME[side], face, NAME[facing1])
        print(NAME[pair_side], pair_face, NAME[facing2])
        print()
        for _ in range(side_length):
            seams[pos1, side] = pos2, opposite_facing(side)
            seams[pos2, pair_side] = pos1, opposite_facing(pair_side)
            pos1 = add_tuples(pos1, dir1)
            pos2 = add_tuples(pos2, dir2)
    pprint.pp(seams)
    print(len(seams))
    return seams


def is_in_map(_map, position):
    row, col = position
    return row >= 0 and row < len(_map) and col >= 0 and col < len(_map[row])


def parse_instructions(instructions):
    parts = []
    prev = 0
    curr = 0
    while curr < len(instructions):
        if instructions[curr].isalpha():
            parts.append(int(instructions[prev:curr]))
            parts.append(instructions[curr : curr + 1])
            prev = curr + 1
        curr += 1
    parts.append(int(instructions[prev:]))
    return parts


def change_facing(facing, turn):
    if turn == "R":
        return (facing + 1) % 4
    if turn == "L":
        return (facing - 1) % 4


def opposite_direction(facing):
    return facing_direction(opposite_facing(facing))


def opposite_facing(facing):
    return (facing + 2) % 4


def facing_direction(facing):
    if facing == RIGHT:
        return 0, 1
    if facing == DOWN:
        return 1, 0
    if facing == LEFT:
        return 0, -1
    if facing == UP:
        return -1, 0


def get_map_and_instructions():
    _map = []
    instructions = None
    map_finished = False
    for line in fileinput.input():
        line = line[:-1]
        if not line:
            map_finished = True
            continue
        if map_finished:
            instructions = line
        else:
            _map.append(line)
    return _map, instructions


if __name__ == "__main__":
    main()
