from typing import List
import time
from pygame.constants import *
from fui import WindowManager
from greedy_central_solution import GreedyCentralSolution
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType


class ForwardPursueNode(Node):
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, pursue_target=None):
        #
        # if type(in_node) is type(Node):
        #     self = in_node

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

        self.proof = GreedyCentralSolution(self.unit_distance * .8)

    @property
    def environment(self):
        accumulator = []
        for x in self.__a + self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance * 1.2:
                    accumulator.append(x)
        return accumulator

    def follow(self):
        if self.type is NodeType.Relay:
            # a propegated velocity is used to move everything around

            print("follow works")
            self.proof.node_list = self.environment

            self.move_along_line(self.angle_to(self.pursue_target),
                                 (self.distance_to(self.pursue_target) - self.unit_distance) * .2)

            try:
                self.proof.execute_pipeline()
                self.move_along_line(self.angle_to(self.proof.relay_list[0]),
                                     self.distance_to(self.proof.relay_list[0]) * .2)
                self.proof.reset()
            except:
                pass

        elif self.type is NodeType.Home:
            if self.distance_to(self.pursue_target) > self.unit_distance * .8:
                new_node = ForwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance,
                                             in_node=Node(Pos(0, 0)))

                new_node.type = NodeType.Relay
                new_node.move_along_line(new_node.angle_to(self.pursue_target),
                                         self.distance_to(self.pursue_target) * .8)

                new_node.pursue_target = self.pursue_target
                self.pursue_target = new_node
                self.__global_relay_link.append(new_node)

            # if in call-back range
            if self.distance_to(self.pursue_target) < self.unit_distance * .1:
                current_target = self.pursue_target
                self.pursue_target = current_target.pursue_target
                try:

                    self.__global_relay_link.remove(current_target)
                    print("triggered from the bottom")
                except Exception as e:
                    print(e)
                    print("Node removal error")


class ForwardDecentralizedSolution(NodeNetwork):
    home_node: Node
    relay_list = List[ForwardPursueNode]

    def __init__(self, unit_distance, full_list=None):
        self.unit_distance = unit_distance
        self.home_node = None

        self.__sandbox = None

        super().__init__()

        # a little trick to get the start node in the iteration without having to do alot of array copy..
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
    node_selector = 1

    move_coefficient = 10

    # create a list of nodes, this is our scenario
    node_list = []
    a_node = Node(Pos(0, 0))
    b_node = Node(Pos(1.7 * 10, 1 * 10))
    c_node = Node(Pos(2 * 10, 2 * 10))

    node_list.append(a_node)
    node_list.append(b_node)
    # node_list.append(c_node)

    # shove the list into a scenario solver
    dist_list = ForwardDecentralizedSolution(40, node_list)
    greedy_list = GreedyCentralSolution(40 * .8, node_list)

    game_window = WindowManager()

    while True:

        # execute the scenario solver
        deltaT = time.time()
        dist_list.execute_pipeline()
        greedy_list.execute_pipeline()
        deltaT = time.time() - deltaT

        # take the solutions into the window rendered
        for x in node_list:
            game_window.nodes.append(x.position.as_int_array)

        game_window.greedy_relays = []
        for x in dist_list.relay_list[1:]:
            game_window.greedy_relays.append(x.position.as_int_array)

        for x in greedy_list.relay_list:
            game_window.pursue_relays.append(x.position.as_int_array)

        game_window.selection = node_list[node_selector].position.as_int_array

        # call the tick/draw function
        game_window.tick(deltaT)

        # add random velocity onto the scenario, except to "base station"
        greedy_list.reset()

        event = game_window.catch_events()

        if event == K_w:
            node_list[node_selector].position.velocity_add([0, move_coefficient])
        if event == K_s:
            node_list[node_selector].position.velocity_add([0, -move_coefficient])
        if event == K_a:
            node_list[node_selector].position.velocity_add([-move_coefficient, 0])
        if event == K_d:
            node_list[node_selector].position.velocity_add([move_coefficient, 0])
        if event == 92:
            print("Attempt to trigger Debugger")

        if event == K_o:
            node_list.append(Node(Pos(0, 0)))

        if event == K_p:
            node_selector += 1
            if node_selector == len(node_list):
                node_selector = 1

        # node_list[1].position.velocity_add([randint(0, 2), randint(0, 2)])
