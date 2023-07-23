import fileinput


class Node:
    """Node in a filesystem tree. Can represent a file or a directory."""

    def __init__(self, name, is_file, size=0):
        self.name = name
        self.is_file = is_file
        self.dirs = []
        self.files = []
        self.size = size if is_file else None

    def __repr__(self):
        if self.is_file:
            return f"File: {self.name} Size: {self.size:,}"
        else:
            return f"Dir: {self.name} Size: {self.size:,} Files: {len(self.files)} Directories: {len(self.dirs)}"

    def add_child(self, child):
        if self.is_file:
            raise TypeError(f"Can't add child {child.name} to file {self.name}")
        if child.is_file:
            self.files.append(child)
        else:
            self.dirs.append(child)

    def update_dir_sizes(self):
        self.size = sum(_file.size for _file in self.files)
        for _dir in self.dirs:
            _dir.update_dir_sizes()
        self.size += sum(_dir.size for _dir in self.dirs)
        print(self)

    def dirs_less_than(self, limit):
        res = 0
        if self.size <= limit:
            print(self)
            res += self.size
        for _dir in self.dirs:
            res += _dir.dirs_less_than(limit)
        return res


def main():
    curr = None
    cwd = []
    for line in fileinput.input():
        line = line.strip()
        if line.startswith("$ cd .."):
            curr = cwd.pop()
            continue
        if line.startswith("$ cd"):
            name = line.split("$ cd ")[1]
            child = Node(name, False)
            if curr:
                curr.add_child(child)
                cwd.append(curr)
            curr = child
            continue
        if line.startswith("$ ls"):
            continue
        if line.startswith("dir"):
            dirname = line.split("dir ")[1]
            continue
        size, filename = line.split()
        curr.add_child(Node(filename, True, int(size)))
    root = cwd[0]
    root.update_dir_sizes()
    print()
    print(root.dirs_less_than(100_000))


if __name__ == "__main__":
    main()
