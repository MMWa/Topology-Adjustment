from enum import Enum, auto
from typing import List
from simulation.node import Node, Pos
from simulation.node.Node import NodeType


class BackwardPursueNode(Node):
    pursue_target: Node
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, pursue_target=None):
        self.__a, self.__b = environment
        self.pursue_target = pursue_target
        self.unit_distance = unit_distance

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

    @property
    def environment(self):
        accumulator = []
        for x in self.__a + self.__b:
            print(self.distance_to(x))
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance:
                    accumulator.append(x)

        return accumulator

    def follow(self):
        if self.distance_to(self.pursue_target) > self.unit_distance * .95:

            if self.type is NodeType.Relay:
                self.move_along_line(self.angle_to(self.pursue_target), self.unit_distance / 8)

            elif self.type is NodeType.Home:
                new_node = BackwardPursueNode([self.__a, self.__b], self.unit_distance, in_node=Node(Pos(0, 0)))

                new_node.type = NodeType.Relay
                new_node.move_along_line(new_node.angle_to(self.pursue_target),
                                         self.distance_to(self.pursue_target) * .9)

                new_node.pursue_target = self.pursue_target
                self.pursue_target = new_node
                self.__b.append(new_node)


if __name__ == "__main__":
    node_list = []
    node_list.append(Node(Pos(0, 0)))
    node_list.append(Node(Pos(1, 1.5)))
    node_list.append(Node(Pos(3, 3)))

    new_test = Node(Pos(1, 1))
    ai_test = BackwardPursueNode(node_list, 2, in_node=Node(Pos(1, 1)))
    print(ai_test.environment)

    print("Dont mess with the order -.-")
