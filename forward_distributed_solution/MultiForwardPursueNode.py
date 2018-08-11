from enum import Enum, auto
from typing import List

from greedy_central_solution import GreedyCentralSolution
from simulation.node import Node, Pos
from simulation.node.Node import NodeType


class MultiForwardPursueNode(Node):
    pursue_target: List[Node]
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, pursue_target=None):
        self.__a, self.__global_relay_link = environment
        self.pursue_target = []
        if pursue_target is not None:
            self.pursue_target.append(pursue_target)

        self.unit_distance = unit_distance

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

        self.proof = GreedyCentralSolution(self.unit_distance * .8)


    @property
    def environment(self):
        accumulator = []
        for x in self.__a + self.__global_relay_link:
            print(self.distance_to(x))
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance:
                    accumulator.append(x)

        return accumulator

    def follow(self):
        for x in self.pursue_target:
            if self.distance_to(x) > self.unit_distance * .8:
                if self.type is NodeType.Relay:
                    self.move_along_line(self.angle_to(x), (self.distance_to(x) - self.unit_distance) * .2)

                    try:
                        self.proof.execute_pipeline()
                        self.move_along_line(self.angle_to(self.proof.relay_list[0]),
                                             self.distance_to(self.proof.relay_list[0]) * .6)
                        self.proof.reset()
                    except:
                        pass



                elif self.type is NodeType.Home:
                    for r in self.__global_relay_link[1:]:
                        if x.distance_to(r) < self.unit_distance * .7:
                            r.pursue_target.append(x)
                            self.pursue_target.remove(x)
                            if r not in self.pursue_target:
                                self.pursue_target.append(r)
                            break

                    if x in self.pursue_target:
                        new_node = MultiForwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance,
                                                          in_node=Node(Pos(0, 0)))

                        new_node.type = NodeType.Relay
                        new_node.move_along_line(new_node.angle_to(x), self.distance_to(x) * .8)

                        new_node.pursue_target.append(x)
                        # needs work
                        self.pursue_target.remove(x)
                        self.pursue_target.append(new_node)
                        self.__global_relay_link.append(new_node)


if __name__ == "__main__":
    node_list = []
    node_list.append(Node(Pos(0, 0)))
    node_list.append(Node(Pos(1, 1.5)))
    node_list.append(Node(Pos(3, 3)))

    new_test = Node(Pos(1, 1))
    ai_test = MultiForwardPursueNode(node_list, 2, in_node=Node(Pos(1, 1)))
    print(ai_test.environment)

    print("Dont mess with the order -.-")
