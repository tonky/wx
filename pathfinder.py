import unittest


class Node():
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def __repr__(self):
        return self.name

    def link(self, node):
        self.neighbours.add(node)

    def adjacent(self, node=False):
        if not node:
            return sorted(self.neighbours)

        self.link(node)
        node.link(self)


def find_path(head, end, seen=[]):
    path = seen + [head]

    if head == end:
        return [path]

    paths = []

    for node in head.neighbours:
        if node in path:
            continue

        for found in find_path(node, end, path):
            paths.append(found)

    return paths

class TestPath(unittest.TestCase):
    def setUp(self):
        self.a = Node("a")
        self.b = Node("b")
        self.c = Node("c")
        self.d = Node("d")

        self.a.adjacent(self.b)
        self.a.adjacent(self.c)
        self.a.adjacent(self.d)
        self.b.adjacent(self.c)
        self.b.adjacent(self.d)
        self.c.adjacent(self.d)

    def test_full_path(self):
        self.assertTrue([self.a, self.b, self.d] in find_path(self.a, self.d))
        self.assertEqual(len(find_path(self.a, self.d)), 5)

    def test_non_duplicates(self):
        self.d.adjacent(self.a)
        self.b.adjacent(self.d)
        self.assertEqual(self.d.adjacent(), sorted([self.a, self.b, self.c]))

    def test_simple_neighbours(self):
        self.assertEqual(self.a.adjacent(), sorted([self.b, self.c, self.d]))


if __name__ == '__main__':
    unittest.main()
