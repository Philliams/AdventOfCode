from __future__ import annotations

from typing import Dict, Generator, List

from src.aoc2022 import utils


class DirectoryNode:
    """
    Class representing a single directory

    :param dirname: the name of the directory
    :type dirname: str

    :param level: the depth of the directory in the tree structure
    :type level: int
    """

    def __init__(self, dirname: str, level: int):
        self.files: List[FileNode] = []
        self.children: Dict[DirectoryNode] = {}
        self.dirname: str = dirname
        self.parent: DirectoryNode = None
        self.level: int = level
        self.size: int = 0

    def add_child(self, child: DirectoryNode):
        """
        Add a child directory to this directory

        :param child: child directory to add
        :type child: DirectoryNode
        """
        if child.dirname not in self.children:
            self.children[child.dirname] = child
            child.parent = self

    def get_child(self, dirname: str):
        """
        Get a child directory by name

        :param dirname: name of child directory to retrieve
        :type dirname: str
        """
        return self.children[dirname]

    def update_size(self, updated_size: int):
        """
        Update the size of this directory

        :param updated_size: number of bytes to add to current size
        :type updated_size: int
        """
        self.size += updated_size
        if self.parent is not None:
            self.parent.update_size(updated_size)

    def add_file(self, file: FileNode):
        """
        Add a child file to this directory

        :param child: child file to add
        :type child: FileNode
        """
        self.files.append(file)
        self.update_size(file.filesize)

    def __repr__(self) -> str:

        num_spaces_per_tab = 4
        prefix = " " * self.level * num_spaces_per_tab

        repr_str = f"DIR: {self.dirname} ({self.size})\n"
        if len(self.children) > 0:
            repr_str += f"{prefix}subdirs:\n"
            for k, v in self.children.items():
                repr_str += f"{prefix}- {v}\n"
        if len(self.files) > 0:
            repr_str += f"{prefix}files:\n"
            for f in self.files:
                repr_str += f"{prefix}- {f}\n"
        return repr_str


class FileNode:
    """
    Class representing a single file

    :param filesize: the size of the file in bytes
    :type filesize: int

    :param filename: the name of the file
    :type filename: str
    """

    def __init__(self, filesize: int, filename: str):
        self.filesize: int = filesize
        self.filename: int = filename

    def __repr__(self) -> str:
        return f"FILE : {self.filename} {self.filesize}"


def parse_data_to_tree(raw_data: str) -> DirectoryNode:
    """
    Parse the raw data into a tree-structure representing the nodes and files

    :param raw_data: Raw data containing commands
    :type raw_data: str

    :return: Root of the directory tree
    :rtype: DirectoryNode
    """
    # get all commands, skip first line for root dir
    lines = raw_data.split("\n")[1:]

    root = DirectoryNode("/", 0)
    current = root

    for line in lines:
        match line.split(" "):  # noqa
            case ["$", "cd", ".."]:  # noqa: E211
                current = current.parent
            case ["$", "cd", "/"]:  # noqa: E211
                current = root
            case ["$", "cd", dirname]:  # noqa: E211
                current = current.get_child(dirname)  # noqa: F821
            case ["$", "ls"]:  # noqa: E211
                pass
            case ["dir", str(dirname)]:  # noqa: E211
                level = current.level + 1
                child_node = DirectoryNode(dirname, level)  # noqa: F821
                current.add_child(child_node)  # noqa: F821
            case [str(num_bytes), str(filename)]:  # noqa: E211
                file_node = FileNode(int(num_bytes), filename)  # noqa: F821
                current.add_file(file_node)
    return root


def tree_iterator(node: DirectoryNode) -> Generator[DirectoryNode, None, None]:
    """
    Produces a generator for traversing the directory/file tree

    :param node: node to traverse
    :type node: DirectoryNode

    :return: Generator for traversing the directory/file tree
    :rtype: Generator[DirectoryNode]
    """
    yield node
    for k, v in node.children.items():
        yield from tree_iterator(v)


def get_directories_under_size(root: DirectoryNode, max_size: int) -> int:
    """
    Calculates the sum of directory sizes for all directories with a max
    size under the given threshold

    :param root: root node for the directory/file tree
    :type root: DirectoryNode

    :param max_size: maximum allowable size for a directory to be kept
    :type max_size: int

    :return: sum of total sizes for directories smaller than max_size
    :rtype: int
    """
    valid_dirs = [d for d in tree_iterator(root) if d.size <= max_size]
    return sum([d.size for d in valid_dirs])


def get_smallest_directory_to_delete(
    root: DirectoryNode, total_space: int, needed_space: int
) -> int:
    """
    Find the smallest directory to delete to free the needed space

    :param root: root node for the directory/file tree
    :type root: DirectoryNode

    :param total_space: total space of the storage device
    :type total_space: int

    :param needed_space: amount of free space required
    :type needed_space: int

    :return: size of the directory to delete
    :rtype: int
    """
    actual_capacity = total_space - root.size
    missing_capacity = needed_space - actual_capacity
    node_iter = tree_iterator(root)
    delete_candidates = [d for d in node_iter if d.size >= missing_capacity]
    return min([d.size for d in delete_candidates])


if __name__ == "__main__":  # pragma: no cover

    data = utils.get_raw_data("./src/aoc2022/data/day7.txt")

    tree_root = parse_data_to_tree(data)

    res = get_directories_under_size(tree_root, 100_000)

    print(f"The total size of directories under 100_000 bytes is {res}")

    res = get_smallest_directory_to_delete(tree_root, 70_000_000, 30_000_000)

    print(f"The size of the smallest directory that can be deleted is {res}")
