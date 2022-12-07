from src.aoc2022.days import day7


def get_sample_raw_data():
    sample_data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    return sample_data


def get_sample_directory_structure():
    i = day7.FileNode(584, "i")
    f = day7.FileNode(29116, "f")
    g = day7.FileNode(2557, "g")
    hlst = day7.FileNode(62596, "h.lst")
    btxt = day7.FileNode(14848514, "b.txt")
    cdat = day7.FileNode(8504156, "c.dat")
    j = day7.FileNode(4060174, "j")
    dlog = day7.FileNode(8033020, "d.log")
    dext = day7.FileNode(5626152, "d.ext")
    k = day7.FileNode(7214296, "k")

    a = day7.DirectoryNode("a", 1)
    e = day7.DirectoryNode("e", 2)
    d = day7.DirectoryNode("d", 1)
    root = day7.DirectoryNode("/", 0)

    root.children = {
        "a": a,
        "d": d,
    }
    root.files = [btxt, cdat]
    root.size = 48381165

    a.children = {"e": e}
    a.files = [f, g, hlst]
    a.size = 94853

    e.children = {}
    e.files = [i]
    e.size = 584

    d.children = {}
    d.files = [j, dlog, dext, k]
    d.size = 24933642

    return root


class TestDay7:
    def test_parse_data_to_tree(self):
        # Prepare

        def files_equal(f1, f2):
            same_name = f1.filename == f2.filename
            same_size = f1.filesize == f2.filesize
            return same_name and same_size

        def directories_equal(d1, d2):
            same_name = d1.dirname == d2.dirname
            same_keys = d1.children.keys() == d2.children.keys()
            same_children = True
            for k in d1.children.keys():
                c1 = d1.children[k]
                c2 = d2.children[k]

                same_children = same_children and directories_equal(c1, c2)

            same_length = len(d1.files) == len(d2.files)
            same_files = True
            for i in range(len(d1.files)):
                f1 = sorted(d1.files, key=lambda f: f.filename)[i]
                f2 = sorted(d2.files, key=lambda f: f.filename)[i]
                same_files = same_files and files_equal(f1, f2)

            same_level = d1.level == d2.level

            return (
                same_name
                and same_keys
                and same_children
                and same_length
                and same_files
                and same_level
            )

        expected_directory_structure = get_sample_directory_structure()
        sample_data = get_sample_raw_data()

        # Run
        actual_directory_structure = day7.parse_data_to_tree(sample_data)

        # Assert
        assert directories_equal(
            expected_directory_structure, actual_directory_structure
        )

    def test_print_directory_structure(self):
        # Prepare
        sample_dir = get_sample_directory_structure()
        expected_output = """DIR: / (48381165)
subdirs:
- DIR: a (94853)
    subdirs:
    - DIR: e (584)
        files:
        - FILE : i 584

    files:
    - FILE : f 29116
    - FILE : g 2557
    - FILE : h.lst 62596

- DIR: d (24933642)
    files:
    - FILE : j 4060174
    - FILE : d.log 8033020
    - FILE : d.ext 5626152
    - FILE : k 7214296

files:
- FILE : b.txt 14848514
- FILE : c.dat 8504156
"""
        # Run
        actual_output = sample_dir.__repr__()
        # Assert
        assert actual_output == expected_output

    def test_tree_iterator(self):
        # Prepare
        sample_dir = get_sample_directory_structure()
        expected_sequence = [48381165, 94853, 584, 24933642]
        # Run
        actual_sequence = [e.size for e in day7.tree_iterator(sample_dir)]

        # Assert
        assert expected_sequence == actual_sequence

    def test_get_directories_under_size(self):
        # Prepare
        sample_dir = get_sample_directory_structure()
        expected_size = 95437
        max_size = 100_000
        # Run
        actual_size = day7.get_directories_under_size(sample_dir, max_size)

        # Assert
        assert expected_size == actual_size

    def test_get_smallest_directory_to_delete(self):
        # Prepare
        sample_dir = get_sample_directory_structure()
        expected_size = 24933642
        total_capacity = 70_000_000
        needed_capacity = 30_000_000
        # Run
        actual_size = day7.get_smallest_directory_to_delete(
            sample_dir, total_capacity, needed_capacity
        )

        # Assert
        assert expected_size == actual_size
