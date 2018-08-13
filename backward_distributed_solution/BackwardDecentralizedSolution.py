import numpy as np
from typing import List
import time
from pygame.constants import *
from greedy_central_solution import GreedyCentralSolution
from fui import WindowManager
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType


class BackwardPursueNode(Node):
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, follower=None):
        self.__a, self.__global_relay_link = environment
        self.follower = follower
        self.unit_distance = unit_distance
        self.proof = GreedyCentralSolution(self.unit_distance * .8)
        self.last_caller = None

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

    @property
    def environment(self):
        accumulator = []
        for x in self.__a[1:] + self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance * 1.2:
                    accumulator.append(x)
        return accumulator

    @property
    def environment_centroid(self):
        points = list(map(lambda x: x.position.as_array, self.environment))
        points = np.sum(points, axis=0)
        return np.divide(points, len(self.environment))

    def move_to(self, target):
        self.last_caller = target
        if self.type == NodeType.Relay:
            try:
                print("try started")
                self.proof.node_list = self.environment
                self.proof.execute_pipeline()
                self.move_along_line(self.angle_to(self.proof.relay_list[0]),
                                     self.distance_to(self.proof.relay_list[0]) * .6)
                print("try successful")
            except Exception as e:
                # target.follower = self.follower
                # try:
                #     self.__global_relay_link.remove(self)
                # except:
                #     print("tried removing a node")

                print(e)
                # print("try failed - node removed")

            self.proof.reset()

            try:
                if target.last_caller in self.environment:
                    if target.type is NodeType.Relay:
                        the_team = target
                        target.last_caller.follower = self
                        # self.follower = self.follower.follower
                        self.__global_relay_link.remove(the_team)
                        print("this got called")
            except Exception as e:
                print(e)

            self.move_along_line(self.angle_to(target), (self.distance_to(target) - self.unit_distance) * .2)

        if self.type == NodeType.Home:
            if self.distance_to(target) > self.unit_distance * .8:
                self.spawn_to(target)

            # if self.distance_to(target) < self.unit_distance * .1:
            #     try:
            #         self.__global_relay_link.remove(target)
            #         print("triggered from the bottom")
            #     except:
            #         print("form the bottom")

        if self.type == NodeType.End:
            if self.distance_to(target) > self.unit_distance * .8:
                target.follower = self.follower

    def spawn_to(self, target):
        new_node = BackwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance,
                                      in_node=Node(Pos(0, 0)))

        new_node.type = NodeType.Relay
        new_node.move_to(target)

        new_node.follower = self
        target.follower = new_node
        self.__global_relay_link.append(new_node)

    def tick(self):
        if self.type == NodeType.Relay:
            if self.follower.last_caller in self.environment:
                if self.follower.type is NodeType.Relay:
                    the_team = self.follower
                    self.follower.last_caller.follower = self
                    # self.follower = self.follower.follower
                    self.__global_relay_link.remove(the_team)
                    print("this got called")

            self.follower.move_to(self)

        if self.type == NodeType.End:
            # for x in self.environment:
            #     if self.distance_to(self.follower) > self.distance_to(x):
            #         self.follower = x
            self.follower.move_to(self)

        if self.type == NodeType.Home:
            pass
            # i think this code might do nothing
            # for x in self.environment:
            #     if self.distance_to(x) < self.unit_distance * .6:
            #         if x is not self:
            #             x.follower = self


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
            self.relay_list.append(new_node)

    def prepare(self):
        for x in self.node_list[1:]:
            x.follower = self.relay_list[0]

    def execute_pipeline(self):
        for x in self.node_list[1:] + self.relay_list:
            x.tick()

    @property
    def sandbox(self):
        return [self.node_list, self.relay_list]


if __name__ == "__main__":
    node_selector = 1
    move_coefficient = 10
    unit_distance = 40

    # create a list of nodes, this is our scenario
    a_node = Node(Pos(0, 0))

    node_list = []
    node_list.append(a_node)

    # shove the list into a scenario solver
    dist_list = BackwardDecentralizedSolution(unit_distance, node_list)
    greedy_list = GreedyCentralSolution(unit_distance * .8, node_list)

    b_node = Node(Pos(1.7 * 10, 1 * 10))
    c_node = Node(Pos(2 * 10, 2 * 10))

    b_node_back = BackwardPursueNode(dist_list.sandbox, unit_distance, in_node=b_node)
    c_node_back = BackwardPursueNode(dist_list.sandbox, unit_distance, in_node=c_node)

    node_list.append(b_node_back)
    # node_list.append(c_node_back)

    dist_list.prepare()

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
            new_node = BackwardPursueNode(dist_list.sandbox, unit_distance, in_node=Node(Pos(0, 0)))
            new_node.type = NodeType.End
            new_node.follower = dist_list.relay_list[0]
            node_list.append(new_node)

        if event == K_p:
            node_selector += 1
            if node_selector == len(node_list):
                node_selector = 1

        # node_list[1].position.velocity_add([randint(0, 2), randint(0, 2)])
