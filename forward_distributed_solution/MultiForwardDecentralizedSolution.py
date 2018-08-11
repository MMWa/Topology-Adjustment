from typing import List

from greedy_central_solution import GreedyCentralSolution
from simulation.node import NodeNetwork, Node, Pos
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
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance:
                    accumulator.append(x)

        return accumulator

    @property
    def environment_relays(self):
        accumulator = []
        for x in self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance:
                    accumulator.append(x)

        return accumulator

    def follow(self):
        try:
            self.proof.node_list = self.environment
            self.proof.execute_pipeline()
        except:
            pass

        # for x in self.environment_relays:
        #     if self.type is NodeType.Relay:
        #         self.move_along_line(self.angle_to(x), (self.distance_to(x) - self.unit_distance) * .2)
        #         try:
        #             self.move_along_line(self.angle_to(self.proof.relay_list[0]),
        #                                  self.distance_to(self.proof.relay_list[0]) * .2)
        #         except:
        #             pass

        for x in self.pursue_target:
            print("we runnning")
            if self.type is NodeType.Relay:
                self.move_along_line(self.angle_to(x), (self.distance_to(x) - self.unit_distance) * .2)
                try:
                    self.move_along_line(self.angle_to(self.proof.relay_list[0]),
                                         self.distance_to(self.proof.relay_list[0]) * .6)
                    print("it gets triggered")

                except:
                    pass

            elif self.type is NodeType.Home:
                if self.distance_to(x) > self.unit_distance * .8:
                    new_node = MultiForwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance,
                                                      in_node=Node(Pos(0, 0)))

                    new_node.type = NodeType.Relay
                    new_node.move_along_line(new_node.angle_to(x),
                                             self.distance_to(x) * .8)

                    new_node.pursue_target.append(x)
                    self.pursue_target.append(new_node)
                    self.pursue_target.remove(x)
                    self.__global_relay_link.append(new_node)

                # if in call-back range
                if self.distance_to(x) < self.unit_distance * .1:
                    current_target = x
                    little_set = self.pursue_target + current_target.pursue_target
                    self.pursue_target = set(little_set)

                    try:
                        self.__global_relay_link.remove(current_target)
                        print("triggered from the bottom")
                    except:
                        print("form the bottom")

        self.proof.reset()


class MultiForwardDecentralizedSolution(NodeNetwork):
    home_node: Node
    relay_list = List[MultiForwardPursueNode]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        self.home_node = None

        self.__sandbox = None

        super().__init__()

        if full_list is not None:
            self.node_list = full_list
            self.home_node = full_list[0]
            self.home_node.type = NodeType.Home
            new_node = MultiForwardPursueNode([self.node_list, self.relay_list], self.unit_distance,
                                              in_node=self.home_node)
            new_node.type = NodeType.Home
            new_node.pursue_target = self.node_list[1:]
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

    test_dist = MultiForwardDecentralizedSolution(2, node_list)

    # a_relay = MultiForwardPursueNode(test_dist.sandbox, 2, in_node=Node(Pos(1, 1)))
    # a_relay.type = NodeType.Relay

    # node_list.append(c_node)

    # test_dist.relay_list.append(a_relay)
    # print(a_relay.environment)
    print(test_dist.sandbox)

    test_dist.execute_pipeline()

    test_dist.to_plot()

    # print(test_dist.home_node.distance_to(b_node))
