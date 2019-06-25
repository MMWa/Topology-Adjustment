import random

import numpy as np
from typing import List
import time
from pygame.constants import *

from decentralized_solution.messenger import Messenger, Message
from greedy_central_solution import GreedyCentralSolution
from fui import WindowManager, WindowManagerTypeTwo
from simulation.node import NodeNetwork, Node, Pos
from simulation.node.Node import NodeType
import logging

COMPRESSION_DECOMPRESSION_FIX = True


class DecentralizedNode(Node):
    __environment: List[Node]

    def __init__(self, environment, unit_distance, position=None, in_node=None, parent=None, node_name=None):
        self.__a, self.__global_relay_link = environment
        self.parent = parent
        self.children = []
        self.endpoints = []
        self.endpoints_freshness = []
        self.announcement_counter = 0

        self.messenger = Messenger(node_name)
        # self.perceived_environment = NodeRecord()

        self.unit_distance = unit_distance
        self.critical_range = self.unit_distance
        self.safe_range = self.unit_distance * 0.8
        self.max_velocity = 10
        self.max_random_velocity = self.unit_distance / 50

        self.proof = GreedyCentralSolution(self.unit_distance)
        self.depth = 0
        self.__issue_counter = 0

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
        self.node_name = self.ID

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
    def environment_all(self):
        accumulator = []
        for x in self.__a[1:] + self.__global_relay_link:
            if not self.ID == x.ID:
                if x.type is not NodeType.End:
                    accumulator.append(x)
        return accumulator

    def change_parent(self, new_parent):
        try:
            self.parent.remove_child(self)
            self.parent = new_parent
            self.parent.add_child(self)
        except Exception as e:
            print("it happens")

    def immediate_neighborhood(self):
        i_ne = []
        for x in self.children:
            i_ne.append(x)
            for y in x.children:
                i_ne.append(y)
        return i_ne

    @staticmethod
    def check_link(node, me):
        if node is None:
            return False

        if node.type == NodeType.Home:
            return True

        elif node == me:
            return False

        else:
            return node.check_link(node.parent, me)

    def announce_removal(self, target):
        if target in self.children:
            self.children.remove(target)

        for child in self.children:
            child.announce_removal(target)

    def announce_endpoint_exist(self, target):
        if target not in self.endpoints:
            self.endpoints.append(target)
            self.endpoints_freshness.append(0)

        else:
            idx = self.endpoints.index(target)
            self.endpoints_freshness[idx] = 0

        if self.type is not NodeType.Home:
            self.parent.announce_endpoint_exist(target)

    def add_child(self, target):
        if target not in self.children:
            self.children.append(target)

    def remove_child(self, target):
        if target in self.children:
            self.children.remove(target)

    def update_parent(self):
        # turns out backward switching can be removed all together
        # checks for backward reduction
        # if not self.parent.type is NodeType.Home:
        #     try:
        #         if self.distance_to(self.parent.parent) < self.critical_range:
        #             # print(self.distance_to(self.parent.parent))
        #             self.change_parent(self.parent.parent)
        #             # print("parent changed ")
        #     except Exception as e:
        #         print(e)
        #         print("A node doesnt have a parent")

        for x in self.environment_all:
            try:
                if x not in self.immediate_neighborhood():
                    if x is not self.parent:
                        if self.distance_to(x) < self.distance_to(self.parent):
                            if x.type is not NodeType.End:
                                # prevents the the broken link situation
                                if self.check_link(x, self):
                                    self.change_parent(x)
            except Exception as e:
                print(e)

    def move_centroid(self):
        points = list(map(lambda x: x.position.as_array, self.children + [self.parent]))
        p_len = len(points)
        points = np.sum(points, axis=0)
        points = np.divide(points, p_len)
        return points

    def child_centroid(self):
        filtered_children = filter(lambda x: x.type is not NodeType.End, self.children)
        points = list(map(lambda x: x.position.as_array, filtered_children))
        p_len = len(points)
        points = np.sum(points, axis=0)
        points = np.divide(points, p_len)
        return points

    def flood_message(self):
        if self.type == NodeType.Home:
            # make sure depth is zero every time
            self.depth = 0
            self.messenger.node_name = "gateway"

            for child in self.children:
                # child: DecentralizedNode
                child.messenger.receive(Message("hello", "gateway", "endnode"))

    def move_to(self):
        [xs, ys] = self.move_centroid()
        tmp = Node(Pos(xs, ys))
        self.move_along_line(self.angle_to(tmp), min([self.distance_to(tmp), self.max_velocity]))

        if COMPRESSION_DECOMPRESSION_FIX:
            try:
                [xs, ys] = self.child_centroid()
                tmp = Node(Pos(xs, ys))
                self.move_along_line(self.angle_to(tmp),
                                     min([self.distance_to(tmp) - self.critical_range, self.max_velocity]))
            except:
                pass

    def tell_depth(self, value):
        self.depth = value + 1

    def request_parent_proximity(self):
        self.parent.receive_proximity_request(self)

    def request_reduce_density(self):
        if self.parent.type is not NodeType.Home:
            self.parent.receive_reduce_density()

    def receive_proximity_request(self, target):
        if self.type is not NodeType.Home:
            self.move_along_line(self.angle_to(target=target), (self.distance_to(target) - self.critical_range))

    def tick(self):
        # this is a garbage cleaning step
        for child in self.children:
            # internally make sure there is no reference to a non existent node
            if child not in self.__a[1:] + self.__global_relay_link:
                self.children.remove(child)
                break

        self.messenger.process()
        for x in self.messenger.out_queue:
            for y in self.children:
                y.messenger.receive(x)
            self.messenger.out_queue.remove(x)

        for x in self.children:
            x.tell_depth(self.depth)

        for idx, _ in enumerate(self.endpoints):
            self.endpoints_freshness[idx] += 1

        for idx, x in enumerate(self.endpoints_freshness):
            if x > 120:
                del self.endpoints[idx]
                del self.endpoints_freshness[idx]

        if self.type == NodeType.Relay:
            # call the procedures that make decentralized nodes
            self.update_parent()
            self.move_to()
            if not COMPRESSION_DECOMPRESSION_FIX:
                self.request_parent_proximity()

            if not COMPRESSION_DECOMPRESSION_FIX:
                # the random noise added to all relays so they avoid local minima solutions
                self.position.velocity_add([(random.random() * self.max_random_velocity) - (self.max_random_velocity / 2),
                                            (random.random() * self.max_random_velocity) - (self.max_random_velocity / 2)])

            # check if we have multiple children follow only one if two are going in separate directions
            if len(self.children) > 1:
                for child in self.children:
                    if self.distance_to(child) > self.critical_range:
                        # make it only preform this every 20 ticks for stable switching
                        if self.__issue_counter > 20:
                            self.__issue_counter = 0
                            child.change_parent(self.parent)
                            self.change_parent(self.parent.parent)
                            return
                        self.__issue_counter += 1

        if self.type == NodeType.End:
            # the broadcast mechanism to indicate endnode branch
            self.update_parent()
            if self.announcement_counter >= 100:
                self.announcement_counter = 0
                self.announce_endpoint_exist(self)
            self.announcement_counter += 1

        if self.type == NodeType.Home:
            # spawn a relay step
            for x in self.children:
                if self.distance_to(x) > self.critical_range:
                    self.spawn_to(x)
                    return

                # Code to preform the despawn step
                # we measure the distance to parent then despawn if parent is in proximity
                if x.type == NodeType.Relay:
                    if x.children:
                        try:
                            [x_cc, y_cc] = x.child_centroid()
                            cc_as_node = Node(Pos(x_cc, y_cc))
                            if self.distance_to(cc_as_node) < self.critical_range:
                                for y in x.children:
                                    y.change_parent(self)
                                    self.announce_removal(x)
                                    self.__global_relay_link.remove(x)
                        except Exception as e:
                            # this is reached if there is an issue with removing a node from __global_relay_link
                            pass

                # if self.distance_to(x) < self.safe_range * 0.5:
                #     for y in x.children:
                #         y.change_parent(self)
                #     if x.type == NodeType.Relay:
                #         try:
                #             self.announce_removal(x)
                #             self.__global_relay_link.remove(x)
                #         except Exception as e:
                #             print(e)
                #             print("Node removal error")
                #         return

    def spawn_to(self, target):
        new_node = DecentralizedNode([self.__a, self.__global_relay_link], self.unit_distance,
                                     in_node=Node(Pos(0, 0)))

        new_node.type = NodeType.Relay

        new_node.parent = self
        new_node.children.append(target)

        self.children.remove(target)
        self.children.append(new_node)

        target.parent = new_node

        new_node.move_to()

        self.__global_relay_link.append(new_node)


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
            new_node.parent = new_node
            self.relay_list.append(new_node)

    def prepare(self):
        for x in self.node_list[1:]:
            x.messenger.node_name = "endnode"
            self.relay_list[0].children.append(x)
            x.parent = self.relay_list[0]

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
    dist_list = DecentralizedSolution(unit_distance, node_list)
    greedy_list = GreedyCentralSolution(unit_distance, node_list)

    d_node = Node(Pos(2 * 10, 0 * 10))
    d_node_back = DecentralizedNode(dist_list.sandbox, unit_distance, in_node=d_node)

    node_list.append(d_node_back)

    dist_list.prepare()
    terminal_mode = False
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
        game_window.greedy_relays = dist_list.relay_list
        if greed_comparer:
            for x__ in greedy_list.relay_list:
                game_window.pursue_relays.append(x__.position.as_int_array)

        game_window.selection = node_list[node_selector].position.as_int_array

        # call the tick/draw function
        game_window.tick(deltaT)
        if greed_comparer:
            greedy_list.reset()

        if not terminal_mode:
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
            if event == K_t:
                dist_list.relay_list[0].flood_message()

            if event == K_o:
                new_node = DecentralizedNode(dist_list.sandbox, unit_distance, in_node=Node(Pos(0, 0)))
                new_node.type = NodeType.End
                new_node.messenger.node_name = "endnode"
                new_node.parent = dist_list.relay_list[0]
                # new_node.parent.children.append(new_node)
                node_list.append(new_node)

            if event == K_p:
                node_selector += 1
                if node_selector == len(node_list):
                    node_selector = 1
        else:
            game_window.event_pump()
            terminal_mode = not terminal_mode

        # node_list[1].position.velocity_add([randint(0, 2), randint(0, 2)])
