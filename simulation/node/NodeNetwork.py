from typing import List
import numpy as np
from simulation.node import Node, Pos
from simulation.IPMaker import IPMaker

__author__ = "Mohamed Wahba (MMWa)"
__version__ = "1.0"
__maintainer__ = "MMWa"

"""
    This file contains the calculations for the central solution, 
    used to calculate the closest to optimum network topology.
    
    NodeNetwork - is a class that handles the calculations and 
    integrating the nodes with the calculations
"""


class NodeNetwork:
    relay_list: List[Node]
    node_list: List[Node]

    def __init__(self):
        self.node_list = []
        self.relay_list = []
        self.address_provider = IPMaker()

    def add(self, new_node: Node = None):
        if new_node is None:
            self.node_list.append(Node(None, self.address_provider.get_address()))
        else:
            self.node_list.append(new_node)

    @property
    def list(self):
        return self.node_list

    def execute_pipeline(self):
        pass

    def reset(self):
        """
        returns the network to an processed state
        """
        self.relay_list = []

    def to_points(self):
        relay_pos = []
        for x in self.relay_list:
            relay_pos.append(x.position.as_array)

        node_pos = []
        for x in self.node_list:
            node_pos.append(x.position.as_array)

        return node_pos, relay_pos

    def to_file(self):
        node_pos, relay_pos = self.to_points()

        np.savetxt('relay-list.csv', relay_pos, delimiter=',')
        np.savetxt('node-list.csv', node_pos, delimiter=',')

    def to_plot(self):
        node_pos, relay_pos = self.to_points()

        relay_pos = np.array(relay_pos)
        node_pos = np.array(node_pos)

        import matplotlib.pyplot as plt
        plt.scatter(node_pos[:, 0], node_pos[:, 1], c="r")
        plt.scatter(relay_pos[:, 0], relay_pos[:, 1], c="b")

        plt.axis('equal')
        plt.show()


if __name__ == "__main__":
    test_list = NodeNetwork()

    test_list.add(Node(Pos(0, 0)))
    test_list.add(Node(Pos(10, 11)))
    test_list.add(Node(Pos(9, 20)))
    test_list.add(Node(Pos(25, 18)))
    test_list.add(Node(Pos(2, 15)))
    test_list.add(Node(Pos(18, -5)))
    test_list.add(Node(Pos(25, 25)))
    test_list.add(Node(Pos(-5, 25)))

    print(test_list.list)
