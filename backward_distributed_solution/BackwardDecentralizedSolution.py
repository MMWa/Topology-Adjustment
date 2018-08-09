from typing import List

from backward_distributed_solution.BackwardPursueNode import BackwardPursueNode
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType


class BackwardDecentralizedSolution(NodeNetwork):
    home_node: Node
    relay_list = List[BackwardPursueNode]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        self.home_node = None

        self.__sandbox = None

        super().__init__()

        if full_list is not None:
            self.node_list = full_list
            self.home_node = full_list[0]
            self.home_node.type = NodeType.Home
            new_node = BackwardPursueNode([self.node_list, self.relay_list], self.unit_distance, in_node=self.home_node)
            new_node.type = NodeType.Home
            new_node.pursue_target = self.node_list[1]
            self.relay_list.append(new_node)

    def execute_pipeline(self):
        for x in self.relay_list:
            x.follow()

    @property
    def sandbox(self):
        return [self.node_list, self.relay_list]


if __name__ == "__main__":
    # create a list of nodes, this is our scenario
    node_list = []

    a_node = Node(Pos(0, 0))
    b_node = Node(Pos(1.7, 1))
    c_node = Node(Pos(1.3, 1))

    node_list.append(a_node)
    node_list.append(b_node)

    test_dist = BackwardDecentralizedSolution(2, node_list)

    # a_relay = MultiForwardPursueNode(test_dist.sandbox, 2, in_node=Node(Pos(1, 1)))
    # a_relay.type = NodeType.Relay

    # node_list.append(c_node)

    # test_dist.relay_list.append(a_relay)
    # print(a_relay.environment)
    print(test_dist.sandbox)

    test_dist.solve()

    test_dist.to_plot()

    # print(test_dist.home_node.distance_to(b_node))
