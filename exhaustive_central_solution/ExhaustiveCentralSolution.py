from typing import List

import numpy as np
from tqdm import tqdm

from exhaustive_central_solution.ExhaustiveNode import ExhaustiveNode
from simulation.node import Node, Pos
from simulation.node.NodeNetwork import NodeNetwork

__author__ = "Mohamed Wahba (MMWa)"
__version__ = "1.0"
__maintainer__ = "MMWa"


class ExhaustiveCentralSolution(NodeNetwork):
    __search_space: List[Node]

    # extra type assertion for intellisense
    relay_list: List[Node]
    node_list: List[Node]

    def __init__(self, unit_distance, full_list=None):
        self.__search_space = []
        self.unit_distance = unit_distance
        self.grid_resolution = 3
        self.max_iterations = 100

        self.a = Pos(-7, -7)
        self.b = Pos(27, 27)

        super().__init__()
        if full_list is not None:
            self.node_list = full_list

    def execute_pipeline(self):
        self.exhaust()
        self.reduce()

    def reduce(self):
        pass

    def exhaust(self):

        mean = []
        for i in self.node_list:
            mean.append(i.position.as_array)

        [x, y] = np.mean(mean, axis=0)

        start_point = ExhaustiveNode(Pos(x, y))
        self.relay_list.append(start_point)
        self.PointsInCircum(start_point, self.unit_distance)

        # recursion because a pointer to the array is used
        # it keeps changing size every time we run
        # the exit condition is no new items
        for i in tqdm(self.relay_list):
            self.PointsInCircum(i, self.unit_distance)
            self.to_plot()

            holder = list(map(lambda x: x.data, self.node_list))
            if all(holder):
                break

    def PointsInCircum(self, reference: Node, radius):

        n = np.multiply(2, np.pi)

        # will always give 6, maybe a useless piece of code
        n_i = int(np.floor(n))

        for i in range(0, n_i):

            h = 2 * np.pi / radius * i
            h = [np.cos(h), np.sin(h)]
            h = np.multiply(h, radius)
            h = np.add(reference.position.as_array, h)

            # if we want a grid locking kind of situation
            # h = np.floor(h)
            # ------------------------------------------

            h = ExhaustiveNode(Pos(h[0], h[1]))
            # print(reference.distance_to(h))
            break_flag = not h.inside_box(self.a, self.b)

            # prove redundancy
            for x in self.relay_list:
                if x.distance_to(h) < radius:
                    if not np.isclose(radius, x.distance_to(h)):
                        break_flag = True
                        break

            for x in self.node_list:

                if np.isclose(x.distance_to(h), 0):
                    break_flag = True
                    break

            if not break_flag:
                self.relay_list.append(h)

                for x in self.node_list:
                    if x.distance_to(h) <= radius:
                        x.data_set()
                        # we also return that node for later processing
                        return h


if __name__ == "__main__":
    test_list = ExhaustiveCentralSolution(3)

    test_list.add(Node(Pos(0, 0)))
    test_list.add(Node(Pos(10, 11)))
    test_list.add(Node(Pos(9, 20)))
    test_list.add(Node(Pos(25, 18)))
    # test_list.add(Node(Pos(2, 15)))
    # test_list.add(Node(Pos(18, -5)))
    # test_list.add(Node(Pos(25, 25)))
    # test_list.add(Node(Pos(-5, 25)))

    test_list.exhaust()

    # start = time.time()
    # test_list.execute_pipeline()
    # end = time.time()
    # print("execution time - " + str(end - start))

    test_list.to_plot()
