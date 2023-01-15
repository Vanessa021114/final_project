from typing import List
from collections import namedtuple
import time


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):

    """
    location: Point
    location: Point
    left: Node
    right: Node
    """

    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0
        self.axis_index = 0
        self.search_loc = None
        self.ans = []

    def insert(self, p: List[Point], depth):
        if depth == 0:
            average_a = 0
            average_b = 0
            for i in p:
                average_a += i.x
                average_b += i.y
            average_a /= len(p)
            average_b /= len(p)
            s_a = 0
            s_b = 0
            for i in p:
                s_a += (i.x - average_a) * (i.x - average_a)
                s_b += (i.y - average_b) * (i.y - average_b)
            # print(s_a, s_b)
            if s_a > s_b:
                p.sort(key=lambda x: x.x)
                mid = len(p) // 2
                self._root = Node(
                    location = p[mid],
                    left = self.insert(p[:mid], depth + 1),
                    right = self.insert(p[mid + 1:], depth + 1)
                )

            else:
                self.axis_index = 1
                p.sort(key=lambda x: x.y)
                mid = len(p) // 2
                self._root = Node(
                    location = p[mid],
                    left = self.insert(p[:mid], depth + 1),
                    right = self.insert(p[mid + 1:], depth + 1)
                )
        else: 
            if (depth % 2 == self.axis_index) and p:
                p.sort(key=lambda x: x.x)
                mid = len(p) // 2
                return Node(
                    location = p[mid],
                    left = self.insert(p[:mid], depth + 1),
                    right = self.insert(p[mid + 1:], depth + 1)
                )
            elif (depth % 2 != self.axis_index) and p:
                p.sort(key=lambda x: x.y)
                mid = len(p) // 2
                return Node(
                    location = p[mid],
                    left = self.insert(p[:mid], depth + 1),
                    right = self.insert(p[mid + 1:], depth + 1)
                )

    def range(self, rectangle: Rectangle) -> List[Point]:
        self.search_loc = self._root
            # print(self.search_loc)
        search_stack = [self.search_loc]
        search_layer = [0]
        while search_stack != []:
            now_search_loc = search_stack.pop()
            now_layer = search_layer.pop()
            if rectangle.is_contains(now_search_loc.location):
                self.ans.append(now_search_loc.location)
                # print(now_search_loc.location)
            if self.axis_index == now_layer % 2:
                if now_search_loc.location.x >= rectangle.lower.x and now_search_loc.left is not None:
                    search_stack.append(now_search_loc.left)
                    search_layer.append(now_layer+1)
                    # print(f'searching{now_search_loc.left.location}')
                if now_search_loc.location.x <= rectangle.upper.x and now_search_loc.right is not None:
                    search_stack.append(now_search_loc.right)
                    search_layer.append(now_layer+1)
                    # print(f'searching{now_search_loc.right.location}')
            else:
                if now_search_loc.location.y >= rectangle.lower.y and now_search_loc.left is not None:
                    search_stack.append(now_search_loc.left)
                    search_layer.append(now_layer+1)
                    # print(f'searching{now_search_loc.left.location}')
                if now_search_loc.location.y <= rectangle.upper.y and now_search_loc.right is not None:
                    search_stack.append(now_search_loc.right)
                    search_layer.append(now_layer+1)
                    # print(f'searching{now_search_loc.right.location}')
        self.search_loc = None
        return self.ans


def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points, 0)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    # print(result)
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    # print(result1)
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points, 0)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    # print(result2)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()
