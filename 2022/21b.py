import fileinput


def main():
    tree = get_tree()
    equation = build_equation(tree)
    value = solve(equation)
    assert verify_value(tree, value)
    print(int(value))


def solve(tree):
    left_root = tree["root"][0]
    right_root = tree["root"][2]
    if is_in(tree, left_root, "humn"):
        node = left_root
        value = get_value(tree, right_root)
    else:
        node = right_root
        value = get_value(tree, left_root)
    while node != "humn":
        left, op, right = tree[node]
        is_in_left = is_in(tree, left, "humn")
        if is_in_left:
            other = get_value(tree, right)
            _next = left
        else:
            other = get_value(tree, left)
            _next = right
        node = _next
        if op == "+":
            value = value - other
        if op == "*":
            value = value / other
        if op == "-":
            if is_in_left:
                value = value + other
            else:
                value = other - value
        if op == "/":
            if is_in_left:
                value = value * other
            else:
                value = value / other
    return value


def verify_value(tree, value):
    tree = tree.copy()
    tree["humn"] = [value]
    left_root = tree["root"][0]
    right_root = tree["root"][2]
    left_value = get_value(tree, left_root)
    right_value = get_value(tree, right_root)
    return left_value == right_value


def build_equation(tree):
    tree = tree.copy()
    humn_parent = [
        node
        for node, data in tree.items()
        if len(data) == 3 and (data[0] == "humn" or data[2] == "humn")
    ][0]
    left_sibling = tree[humn_parent][0]
    right_sibling = tree[humn_parent][2]
    if left_sibling == "humn":
        tree[right_sibling] = [get_value(tree, right_sibling)]
    else:
        tree[left_sibling] = [get_value(tree, left_sibling)]
    tree["humn"] = ["humn"]
    left_root = tree["root"][0]
    right_root = tree["root"][2]
    if is_in(tree, left_root, "humn"):
        tree[right_root] = [get_value(tree, right_root)]
    else:
        tree[left_root] = [get_value(tree, left_root)]
    tree["root"][1] = "=="
    return tree


def get_expression(tree, node):
    data = tree[node]
    if len(data) == 1:
        return str(data[0])
    return (
        "("
        + get_expression(tree, data[0])
        + data[1]
        + get_expression(tree, data[2])
        + ")"
    )


def is_in(tree, start, node):
    if start == node:
        return True
    data = tree[start]
    if len(data) == 1:
        return False
    return is_in(tree, data[0], node) or is_in(tree, data[2], node)


def get_value(tree, node):
    data = tree[node]
    if len(data) == 1:
        return int(data[0])
    value1 = get_value(tree, data[0])
    op = data[1]
    value2 = get_value(tree, data[2])
    if op == "+":
        return value1 + value2
    if op == "*":
        return value1 * value2
    if op == "/":
        return value1 / value2
    if op == "-":
        return value1 - value2


def get_tree():
    tree = {}
    for line in fileinput.input():
        node, _, data = line.strip().partition(": ")
        data = data.split()
        tree[node] = data
    return tree


if __name__ == "__main__":
    main()
