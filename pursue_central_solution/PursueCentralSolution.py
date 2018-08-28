import numpy as np
from typing import List

from simulation.node import NodeNetwork, Node, Pos


class PursueCentralSolution(NodeNetwork):
    # extra type assertion for intellisense
    relay_list: List[Node]
    node_list: List[Node]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        super().__init__()
        if full_list is not None:
            self.node_list = full_list

    def execute_pipeline(self):
        for i in self.node_list[1:]:
            count = int(np.floor(self.node_list[0].distance_to(i) / self.unit_distance))

            [x, y] = self.node_list[0].position.as_array

            for _ in range(count):
                x, y = self.__move_along_line(self.node_list[0].angle_to(i), self.unit_distance, x, y)
                self.relay_list.append(Node(Pos(x, y)))

    @staticmethod
    def __move_along_line(m, s, x, y):
        """
        keep as static
        this really improves performance and gives much more consistent execution time
        """
        g = np.tan(m)

        g_factor = np.square(g)
        g_factor = np.add(1, g_factor)
        g_factor = np.sqrt(g_factor)

        x_o = np.divide(1, g_factor)
        x_o = np.multiply(s, x_o)

        y_o = np.divide(g, g_factor)
        y_o = np.multiply(s, y_o)

        if m > np.pi / 2 or m < - np.pi / 2:
            x_o = np.subtract(x, x_o)
            y_o = np.subtract(y, y_o)
        else:
            x_o = np.add(x, x_o)
            y_o = np.add(y, y_o)
        return x_o, y_o


if __name__ == "__main__":
    test_list = PursueCentralSolution(2)

    test_list.add(Node(Pos(0, 0)))
    test_list.add(Node(Pos(10, 11)))
    test_list.add(Node(Pos(9, 20)))
    test_list.add(Node(Pos(25, 18)))
    test_list.add(Node(Pos(2, 15)))
    test_list.add(Node(Pos(18, -5)))
    test_list.add(Node(Pos(25, 25)))
    test_list.add(Node(Pos(-5, 25)))

    test_list.execute_pipeline()

    test_list.to_plot()
