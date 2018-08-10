import math
from typing import List

from greedy_central_solution import GreedyCentralSolution
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType


class ForwardPursueNode(Node):
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, pursue_target=None):

        if type(in_node) is type(Node):
            self = in_node

        self.__a, self.__global_relay_link = environment
        self.pursue_target = None
        if pursue_target is not None:
            self.pursue_target.append(pursue_target)

        self.unit_distance = unit_distance

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

        self.proof = GreedyCentralSolution(self.unit_distance)


    def environment(self):
        accumulator = []
        for x in self.__a + self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance*1.2:
                    accumulator.append(x)

        return accumulator

    def follow(self):

        # if self.type is NodeType.Home:
        #     print(" this is Home")
        #     print(self.position.as_array)
        #     print(self.distance_to(self.pursue_target))

        if self.type is NodeType.Relay:
            # a propegated velocity is used to move everything around
            """I should try to mimic the pursued velocity, accompanied with some discount factor"""

            self.proof.node_list = self.environment()

            self.move_along_line(self.angle_to(self.pursue_target),
                                 (self.distance_to(self.pursue_target) - self.unit_distance*.95) * .2)

            try:
                self.proof.execute_pipeline()
                self.move_along_line(self.angle_to(self.proof.relay_list[0]), self.distance_to(self.proof.relay_list[0])*.1)
                self.proof.reset()
            except:
                pass


            #self.move_along_sin_rule(self.pursue_target.position.last_velocity,0,0)

        elif self.type is NodeType.Home:
            if self.distance_to(self.pursue_target) > self.unit_distance * .81:
                new_node = ForwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance, in_node=Node(Pos(0, 0)))

                new_node.type = NodeType.Relay
                new_node.move_along_line(new_node.angle_to(self.pursue_target), self.distance_to(self.pursue_target) * .8)

                new_node.pursue_target = self.pursue_target
                self.pursue_target = new_node
                self.__global_relay_link.append(new_node)

            # if in call-back range
            if self.distance_to(self.pursue_target) < self.unit_distance * .4:
                current_target = self.pursue_target
                self.pursue_target = current_target.pursue_target
                self.__global_relay_link.remove(current_target)


class ForwardDecentralizedSolution(NodeNetwork):
    home_node: Node
    relay_list = List[ForwardPursueNode]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        self.home_node = None

        self.__sandbox = None

        super().__init__()

        if full_list is not None:
            self.node_list = full_list
            self.home_node = full_list[0]
            self.home_node.type = NodeType.Home
            new_node = ForwardPursueNode([self.node_list, self.relay_list], self.unit_distance, in_node=self.home_node)
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

    test_dist = ForwardDecentralizedSolution(2, node_list)

    # a_relay = MultiForwardPursueNode(test_dist.sandbox, 2, in_node=Node(Pos(1, 1)))
    # a_relay.type = NodeType.Relay

    # node_list.append(c_node)

    # test_dist.relay_list.append(a_relay)
    # print(a_relay.environment)
    print(test_dist.sandbox)

    test_dist.execute_pipeline()

    test_dist.to_plot()

    # print(test_dist.home_node.distance_to(b_node))

    # new set of test for inheratance


