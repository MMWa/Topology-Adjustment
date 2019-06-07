import numpy as np
from typing import List
import time
from pygame.constants import *
from greedy_central_solution import GreedyCentralSolution
from fui import WindowManager, WindowManagerTypeTwo
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType
import logging


class DecentralizedNode(Node):
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, follower=None):
        self.__a, self.__global_relay_link = environment
        self.follower = follower
        self.unit_distance = unit_distance
        self.proof = GreedyCentralSolution(self.unit_distance)
        self.last_caller = None
        self.depth = 0
        self.__depth_counter = 0
        self.tick_tock = 0
        try:
            self.home = self.__global_relay_link[0]
        except:
            self.home = self

        self.call_counter = 0

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

    @property
    def depth_counter(self):
        if self.type is NodeType.Home:
            self.__depth_counter += 1
            return self.__depth_counter
        else:
            return 0

    @property
    def environment(self):
        accumulator = []
        for x in self.__a[1:] + self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance * 1.2:
                    # if x.type is not NodeType.End:
                    accumulator.append(x)
        return accumulator

    @property
    def environment_infrastructure(self):
        accumulator = []
        for x in self.__a[1:] + self.__global_relay_link:
            if not self.ID == x.ID:
                if self.distance_to(x) < self.unit_distance * 1.2:
                    if x.type is not NodeType.End:
                        accumulator.append(x)
        return accumulator

    @property
    def environment_full(self):
        accumulator = []
        for x in self.__a + self.__global_relay_link:
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
        self.call_counter = 0
        self.last_caller = target
        if self.type == NodeType.Relay:
            # chain tightening code
            self.move_along_line(self.angle_to(target), (self.distance_to(target) - self.unit_distance) * .2)

            try:
                if len(self.environment) is 2:
                    if self.environment[0].distance_to(self.environment[1]) > 0.8 * self.unit_distance:
                        [xs, ys] = self.environment_centroid
                        to_go = Node(Pos(xs, ys))
                        self.move_along_line(self.angle_to(to_go), self.distance_to(to_go) * 0.6)

            except IndexError as e:
                log.error("--------------------------------------------------")
                log.error("try failed - couldn't find a solution")
                log.error(e)
                # # force it for now
                if self.home not in self.environment_full:
                    try:
                        for j in self.follower.environment_infrastructure:
                            if self.last_caller is j:
                                self.last_caller.follower = self
                                self.__global_relay_link.remove(self)

                        self.last_caller.follower = self
                        self.__global_relay_link.remove(self)
                        log.error("Problem solved")
                    except Exception as er:
                        log.error(er)
                        log.error("no hope in this one")

        if self.type == NodeType.Home:
            if self.distance_to(target) > self.unit_distance * .8:
                self.spawn_to(target)

        if self.type == NodeType.End:
            # if self.distance_to(target) > self.unit_distance * .8:
            target.follower = self.follower

    def spawn_to(self, target):
        new_node = BackwardPursueNode([self.__a, self.__global_relay_link], self.unit_distance,
                                      in_node=Node(Pos(0, 0)))

        new_node.type = NodeType.Relay
        new_node.move_to(target)

        new_node.follower = self
        new_node.depth = self.depth_counter
        target.follower = new_node
        self.__global_relay_link.append(new_node)

    def tick(self):
        self.call_counter += 1
        if self.type == NodeType.Relay:
            if self.home not in self.environment_full:
                x: BackwardPursueNode
                for x in self.environment_full:
                    if self.distance_to(x) < self.distance_to(self.follower):
                        if x.distance_to(self.home) <= self.follower.distance_to(self.home) or x.follower is not self:
                        # if x.follower is self:
                            self.follower = x
            # if self.follower in self.environment_full:
            self.follower.move_to(self)
            # if self.call_counter > 40:
            #     self.__global_relay_link.remove(self)

        if self.type == NodeType.End:
            for x in self.environment_infrastructure:
                if self.distance_to(x) < self.distance_to(self.follower):
                    self.follower = x
            self.follower.move_to(self)

        if self.type == NodeType.Home:
            for i in self.environment_infrastructure:
                if self.distance_to(i) < 0.4 * self.unit_distance:
                    for j in self.environment:
                        if i.last_caller is j:
                            i.last_caller.follower = self
                            self.__global_relay_link.remove(i)

if __name__ == "__main__":

    log = logging.getLogger(__name__)
    node_selector = 1
    move_coefficient = 10
    unit_distance = 40

    # create a list of nodes, this is our scenario
    a_node = Node(Pos(0, 0))

    node_list = []
    node_list.append(a_node)

    # shove the list into a scenario solver
    # the way the algorithms work makes for a .85 ratio in comms
    dist_list = BackwardDecentralizedSolution(unit_distance, node_list)
    greedy_list = GreedyCentralSolution(unit_distance, node_list)

    b_node = Node(Pos(1.7 * 10, 1 * 10))
    c_node = Node(Pos(2 * 10, 2 * 10))

    b_node_back = BackwardPursueNode(dist_list.sandbox, unit_distance, in_node=b_node)
    c_node_back = BackwardPursueNode(dist_list.sandbox, unit_distance, in_node=c_node)

    node_list.append(b_node_back)
    # node_list.append(c_node_back)

    dist_list.prepare()

    game_window = WindowManagerTypeTwo()

    while True:
        greed_comparer = True
        # execute the scenario solver
        deltaT = time.time()
        dist_list.execute_pipeline()
        if greed_comparer:
            greedy_list.execute_pipeline()
        deltaT = time.time() - deltaT

        # take the solutions into the window rendered
        game_window.nodes = node_list

        game_window.greedy_relays = []
        game_window.greedy_relays = dist_list.relay_list[1:]
        if greed_comparer:
            for x in greedy_list.relay_list:
                game_window.pursue_relays.append(x.position.as_int_array)

        game_window.selection = node_list[node_selector].position.as_int_array

        # call the tick/draw function
        game_window.tick(deltaT)
        if greed_comparer:
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
            log.error("Attempt to trigger Debugger")

        if event == K_b:
            game_window.environment_toggle = not game_window.environment_toggle
        if event == K_n:
            game_window.follower_toggle = not game_window.follower_toggle
        if event == K_m:
            game_window.caller_toggle = not game_window.caller_toggle

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
