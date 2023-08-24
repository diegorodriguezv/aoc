import fileinput

""" The solution to this problem needs several concepts that represent ideas in 
different levels of abstraction.
Map: 2D representation of the cube. Composed of square faces.
Face: Represented by it's top left coordinate relative to other faces. One unit is the
    length of the side.
Cube: A model of the 3D entity but without using a third dimension. It is modeled by 
    assigning letters to each of it's vertices.
Corners: Represent a face of the cube by enumerating the 4 vertices in a top-bottom,
    left-right order.
Facing: A direction in 2D space. Can also represent an edge of a face, in that case it
    can be called a side.
Direction: A tuple that represents movement or delta in 2D space.
Seam: Is a translation from one position and one direction in a face to another position 
    and another direction in other face. This abstraction allows easy navigation around 
    the edges of a face that has no adjacent face to it.
Turn: Is a change in direction or rotation. Represented by "L" (clockwise) and "R" 
    (clockwise).
Position: A 2D coordinate in the map.
"""

# These are the "facing" or directions
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
NAME = {RIGHT: "RIGHT", DOWN: "DOWN", LEFT: "LEFT", UP: "UP"}


def main():
    _map, instructions = get_map_and_instructions()
    position, facing = follow_instructions(_map, instructions)
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
    """Return the two corners of the face in the edge facing a given direction."""
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


def seam_dir(side):
    """Select a direction to traverse a side of a face."""
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
    for _ in range(4):
        if corners_edge(corners, facing) == corners_edge(
            rotated, opposite_facing(facing)
        ):
            return rotated
        rotated = rotate_corners(rotated, "R")


def wrapped_edges(faces):
    """Assign cube corners to each face (wrap) and return the edges for faces without an
     adjacent face in the map.
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
    work = [(faces[0], cube[0])]
    while work:
        face, corners = work.pop()
        if face in visited:
            continue
        visited.add(face)
        for facing in [RIGHT, DOWN, LEFT, UP]:
            neighbor_face = adjacent_face(face, faces, facing)
            if neighbor_face:
                neighbor_corners = rotated_adjacent_corners(cube, corners, facing)
                work.append((neighbor_face, neighbor_corners))
            else:
                edges[(face, facing)] = corners_edge(corners, facing)
    return edges


def start_point(_map):
    first_col = _map[0].index(".")
    return 0, first_col


def follow_instructions(_map, instructions):
    facing = 0
    position = start_point(_map)
    side_length = get_side_length(_map)
    seams = create_seams(_map, side_length)
    for instruction in instructions:
        if type(instruction) is int:
            position, facing = walk_straight(_map, position, facing, instruction, seams)
        else:
            facing = rotate_facing(facing, instruction)
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
    """Calculate the side length of each face by dividing the total area of the map by
    6 faces and taking the square root."""
    total_area = sum(1 for row in _map for char in row if char != " ")
    return int((total_area / 6) ** 0.5)


def face_map(_map, side_length):
    """Return a list of relative coordinates of faces in a map. One unit is the size
    of a square face."""
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
    """Return the adjacent face in the map in a given direction or None if it doesn't
    exist."""
    adjacent_face = add_tuples(face, facing_direction(facing))
    return adjacent_face if adjacent_face in faces else None


def start_seam_coordinates(face, side, side_length, seam_dir):
    """Returns the start coordinates to traverse a seam in a given direction."""
    face_row, face_col = face
    top, left = face_row * side_length, face_col * side_length
    bottom, right = (face_row + 1) * side_length - 1, (face_col + 1) * side_length - 1
    if side == LEFT:
        return (top, left) if seam_dir != UP else (bottom, left)
    if side == UP:
        return (top, left) if seam_dir != LEFT else (top, right)
    if side == DOWN:
        return (bottom, left) if seam_dir != LEFT else (bottom, right)
    if side == RIGHT:
        return (top, right) if seam_dir != UP else (bottom, right)


def create_seams(_map, side_length):
    """Return the "seams" of the map. Seams is a dictionary where the key is a map
    coordinate and a direction and the value is the new map coordinate and the new
    direction. It represents the transitions or portals through which to walk in the
    edges of faces that have no adjacent face."""
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
        seam_dir1 = seam_dir(side)
        pos1 = start_seam_coordinates(face, side, side_length, seam_dir1)
        dir1 = facing_direction(seam_dir1)
        seam_dir2 = seam_dir(pair_side)
        if edge != pair_edge:
            seam_dir2 = opposite_facing(seam_dir2)
        pos2 = start_seam_coordinates(pair_face, pair_side, side_length, seam_dir2)
        dir2 = facing_direction(seam_dir2)
        for _ in range(side_length):
            seams[pos1, side] = pos2, opposite_facing(pair_side)
            seams[pos2, pair_side] = pos1, opposite_facing(side)
            pos1 = add_tuples(pos1, dir1)
            pos2 = add_tuples(pos2, dir2)
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


def rotate_facing(facing, turn):
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
    return _map, parse_instructions(instructions)


if __name__ == "__main__":
    main()
