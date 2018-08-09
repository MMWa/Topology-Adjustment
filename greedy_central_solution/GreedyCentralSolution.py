import time
from itertools import chain

from numba import *
from typing import List
import numpy as np

from simulation.node.Node import RegisterStates
from simulation.node.NodeNetwork import NodeNetwork
from simulation.node import Node, Pos
from greedy_central_solution.Segment import Segment

__author__ = "Mohamed Wahba (MMWa)"
__version__ = "1.0"
__maintainer__ = "MMWa"

"""
    This file contains the calculations for the central solution, 
    used to calculate the closest to optimum network topology.

    NodeNetwork - is a class that handles the calculations and integrating the nodes with the calculations

"""


class GreedyCentralSolution(NodeNetwork):
    __segment_list: List[Node]
    __hidden_node_list: List[Node]

    # extra type assertion for intellisense
    relay_list: List[Node]
    node_list: List[Node]

    def __init__(self, unit_distance, full_list=None):
        self.__hidden_node_list = []
        self.__segment_list = []
        self.unit_distance = unit_distance
        super().__init__()
        if full_list is not None:
            self.node_list = full_list

    def __find_segments(self):

        # fist make sure segment flag is reset
        for x in self.node_list:
            x.hasSegment = False

        # code for first segment
        temp_hold = []
        for x in self.node_list[1:]:
            temp_hold.append(self.node_list[0].distance_to(x))

        closest = np.argmin(temp_hold)
        self.node_list[0].hasSegment = True
        self.node_list[closest + 1].hasSegment = True

        self.__segment_list.append(Segment(self.node_list[0], self.node_list[closest + 1], temp_hold[closest]))

        # code for the rest
        node_selector = 0
        for _ in self.node_list[1:-1]:
            minDistance = np.inf
            for j in self.__segment_list:
                for i in self.node_list:
                    if not i.hasSegment:
                        newSegment = j.distance_to(i)

                        if newSegment.distance < minDistance:
                            node_selector = i
                            minDistance = newSegment.distance
                            tmp_segment = newSegment
            # there is a risk of reference before assignment here, if the numbers dont play nice
            node_selector.hasSegment = True
            self.__segment_list.append(tmp_segment)

            if tmp_segment.hasHidden:
                self.__hidden_node_list.append(tmp_segment.pointA)

    def __add_relays(self, distance_multiplier):
        for i in self.__segment_list:
            if not i.hasHidden:
                # mVal = np.subtract(i.pointB.position.as_array, i.pointA.position.as_array)
                # mVal = np.arctan2(mVal[1], mVal[0])
                mVal = i.pointA.angle_to(i.pointB)

                [x, y] = i.pointA.position.as_array

                relay_count = int(np.floor(i.distance / distance_multiplier))

                for j in range(relay_count):
                    x, y = self.__move_along_line(mVal, distance_multiplier, x, y)
                    self.relay_list.append(Node(Pos(x, y)))

                i.hasRelays = True

        for i in self.__segment_list:

            if i.hasHidden:
                internal_found = np.inf
                for k in self.relay_list:
                    query_distance = i.pointA.distance_to(k)
                    if query_distance < internal_found:
                        internal_found = query_distance
                        [x, y] = k.position.as_array

                mVal = np.subtract(i.pointB.position.as_array, [x, y])
                mVal = np.arctan2(mVal[1], mVal[0])

                relay_count = int(np.floor(i.distance / distance_multiplier))

                for j in range(relay_count):
                    x, y = self.__move_along_line(mVal, distance_multiplier, x, y)
                    self.relay_list.append(Node(Pos(x, y)))

    @staticmethod
    @jit
    def __move_along_line(m, s, x, y):

        g = np.tan(m)
        """"
        keep as static to allow for vectorization using jit
        this really improves performance and gives much more consistent execution time
        """
        g_factor = np.square(g)
        g_factor = np.add(1, g_factor)
        g_factor = np.sqrt(g_factor)

        x_o = np.divide(1, g_factor)
        x_o = np.multiply(s, x_o)

        y_o = np.divide(g, g_factor)
        y_o = np.multiply(s, y_o)

        if m > np.pi / 2 or m < - np.pi / 2:
            x_o = np.subtract(x, x_o)
            y_o = np.subtract(y, y_o)
        else:
            x_o = np.add(x, x_o)
            y_o = np.add(y, y_o)
        return x_o, y_o

    def execute_pipeline(self):
        """
        The main pipeline start point
        """
        self.__find_segments()
        self.__add_relays(self.unit_distance)

    def reset(self):
        """
        returns the network to an processed state
        """
        self.__hidden_node_list = []
        self.relay_list = []
        self.__segment_list = []


if __name__ == "__main__":
    test_list = GreedyCentralSolution(2)

    test_list.add(Node(Pos(0, 0)))
    test_list.add(Node(Pos(10, 11)))
    test_list.add(Node(Pos(9, 20)))
    test_list.add(Node(Pos(25, 18)))
    test_list.add(Node(Pos(2, 15)))
    test_list.add(Node(Pos(18, -5)))
    test_list.add(Node(Pos(25, 25)))
    test_list.add(Node(Pos(-5, 25)))

    start = time.time()
    test_list.execute_pipeline()
    end = time.time()
    print("execution time - " + str(end - start))
    #
    # # now we run the test
    # # broadcast from node zero
    # test_list.node_list[0].test_register = RegisterStates.sending
    # x: Node
    # loop_state = True
    #
    # while loop_state:
    #     loop_state = False
    #     temp_hold = []
    #
    #     for i in chain(test_list.node_list, test_list.relay_list):
    #         if i.test_register == RegisterStates.no_state:
    #             loop_state = True
    #
    #         if i.test_register == RegisterStates.sending:
    #             temp_hold.append(i)
    #
    #     for x in temp_hold:
    #         for k in chain(test_list.node_list, test_list.relay_list):
    #             dx = x.distance_to(k)
    #             if dx >= test_list.unit_distance and not (x.test_register is RegisterStates.passed):
    #                 k.test_register = RegisterStates.sending
    #                 x.test_register = RegisterStates.passed

    test_list.to_plot()
