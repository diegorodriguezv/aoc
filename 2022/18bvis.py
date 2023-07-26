from vpython import *
import fileinput
import importlib

aoc18 = importlib.import_module("18b")
# the following throws SyntaxError: invalid decimal literal
# from 18b import exterior_faces

index = 0
quads = None


def main():
    global quads
    scene.visible = False
    scene.width = 1000
    scene.height = 600
    shape = aoc18.get_shape()
    x, y, z = dimensions(shape)
    boxes = create_boxes(shape)
    faces = aoc18.exterior_faces(shape)
    print(f"{len(faces)=}")
    quads = create_faces(faces)
    paint_axes(x, y, z)
    scene.center = vec(x / 2, y / 2, z / 2)
    #     scene.bind("mousedown", show_next_face)
    scene.visible = True
    while True:
        rate(3)
        show_next_face()


def show_next_face():
    global index, quads
    #     print(index)
    if index == len(quads):
        index = 0
        for quad in quads:
            quad.visible = False
        return
    if index > 0:
        for v in quads[index - 1].vs:
            v.opacity = 0.3
    #         quads[index - 1].opacity = 0.3
    quads[index].visible = True
    #     quads[index].opacity = 1
    for v in quads[index].vs:
        v.opacity = 1
    index += 1


def show_next_box():
    global index, boxes
    if index == len(boxes):
        index = 0
        for box in boxes:
            box.visible = False
        return
    if index > 0:
        boxes[index - 1].opacity = 0.3
    boxes[index].visible = True
    boxes[index].opacity = 1
    index += 1


def create_boxes(shape):
    boxes = []
    for x, y, z in shape:
        boxes.append(
            box(
                pos=vec(x + 0.5, y + 0.5, z + 0.5),
                visible=True,
                size=vec(0.5, 0.5, 0.5),
            )
        )
    return boxes


def create_faces(faces):
    quads = []
    for cube, normal in faces:
        vertices = get_face_vertices(cube, normal)
        quad = get_quad(vertices, normal)
        quad.visible = False
        quads.append(quad)
    return quads


def get_face_vertices(cube, normal):
    x, y, z = cube
    vertices = [
        (x, y, z),
        (x + 1, y, z),
        (x + 1, y + 1, z),
        (x, y + 1, z),
        (x, y, z + 1),
        (x + 1, y, z + 1),
        (x + 1, y + 1, z + 1),
        (x, y + 1, z + 1),
    ]
    names = aoc18.get_names_by_face()
    if names[normal] == "x+":
        indexes = [1, 2, 6, 5]
    elif names[normal] == "y+":
        indexes = [2, 3, 7, 6]
    elif names[normal] == "z+":
        indexes = [4, 5, 6, 7]
    elif names[normal] == "x-":
        indexes = [0, 4, 7, 3]
    elif names[normal] == "y-":
        indexes = [0, 1, 5, 4]
    elif names[normal] == "z-":
        indexes = [0, 3, 2, 1]
    else:
        print(normal, names[normal])
    return [vertices[i] for i in indexes]


def get_quad(vertices, normal):
    nx, ny, nz = normal
    v_list = []
    # breakpoint()
    for i, (x, y, z) in enumerate(vertices):
        colors = [color.red, color.green, color.blue, color.yellow]
        v = vertex(pos=vec(x, y, z), normal=vec(nx, ny, nz), color=colors[i])
        v_list.append(v)
    return quad(vs=v_list)


def dimensions(shape):
    max_x = max(x for x, y, z in shape)
    max_y = max(y for x, y, z in shape)
    max_z = max(z for x, y, z in shape)
    return max_x, max_y, max_z


def paint_axes(x, y, z):
    L = max(x, y, z) / 2
    R = L / 100
    xaxis = cylinder(
        pos=vec(0, 0, 0), axis=vec(x + 1, 0, 0), radius=R, color=color.yellow
    )
    yaxis = cylinder(
        pos=vec(0, 0, 0), axis=vec(0, y + 1, 0), radius=R, color=color.yellow
    )
    zaxis = cylinder(
        pos=vec(0, 0, 0), axis=vec(0, 0, z + 1), radius=R, color=color.yellow
    )
    k = 1.02
    h = 0.05 * L
    paint_axis_name(xaxis.pos + k * xaxis.axis, "x", h)
    paint_axis_name(yaxis.pos + k * yaxis.axis, "y", h)
    paint_axis_name(zaxis.pos + k * zaxis.axis, "z", h)
    spheres = []
    for i in range(1, x + 1):
        spheres.append(sphere(pos=vec(i, 0, 0), radius=R * 2, color=color.cyan))
    for i in range(1, y + 1):
        spheres.append(sphere(pos=vec(0, i, 0), radius=R * 2, color=color.cyan))
    for i in range(1, z + 1):
        spheres.append(sphere(pos=vec(0, 0, i), radius=R * 2, color=color.cyan))


def paint_axis_name(pos, tex, heigh):
    text(
        pos=pos,
        text=tex,
        height=heigh,
        align="center",
        billboard=True,
        emissive=True,
    )


if __name__ == "__main__":
    main()
