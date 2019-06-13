from simulation.node import NodeNetwork, Node
from decentralized_solution.DecentralizedNode import DecentralizedNode
from typing import List

from simulation.node.Node import NodeType


class DecentralizedSolution(NodeNetwork):
    home_node: Node
    relay_list = List[DecentralizedNode]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        self.home_node = None

        self.__sandbox = None

        super().__init__()

        if full_list is not None:
            self.node_list = full_list
            self.home_node = full_list[0]
            self.home_node.type = NodeType.Home
            new_node = DecentralizedNode([self.node_list, self.relay_list], self.unit_distance, in_node=self.home_node)
            new_node.type = NodeType.Home
            self.relay_list.append(new_node)

    def prepare(self):
        for x in self.node_list[1:]:
            x.follower = self.relay_list[0]

    def execute_pipeline(self):
        for x in self.node_list[1:] + self.relay_list:
            x.tick()

    def reset(self):
        """
        returns the network to an processed state
        """
        self.relay_list = self.relay_list[:1]
        self.relay_list.children = None

    @property
    def sandbox(self):
        return [self.node_list, self.relay_list]
