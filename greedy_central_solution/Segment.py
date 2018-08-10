from numba import *
import numpy as np
from simulation.node.Node import Node
from simulation.node.Pos import Pos


class Segment:
    hasRelays: bool
    hasHidden: bool

    def __init__(self, a: Node, b: Node, distance):
        self.pointA = a
        self.pointB = b
        self.distance = distance
        self.hasHidden = False
        self.hasRelays = True

    @property
    def as_array(self):
        return [self.pointA, self.pointB]

    def distance_to(self, node: Node):

        disA = self.pointA.distance_to(node)
        disB = self.pointA.distance_to(self.pointB)
        disC = self.pointB.distance_to(node)

        # A & C are the distances from segment edges to the NODE
        ac_array = np.sort([disA, disC])

        # theta length calculation
        if ac_array[0] != disA:
            n1 = self.pointA
            theta_length = np.add(np.square(disB), np.square(disC))
            theta_length = np.subtract(theta_length, np.square(disA))

        else:
            n1 = self.pointB
            theta_length = np.add(np.square(disB), np.square(disA))
            theta_length = np.subtract(theta_length, np.square(disC))

        theta_length = np.divide(theta_length, np.prod([2, disB, disC]))
        theta_length = np.arccos(theta_length)
        theta_length = np.absolute(theta_length)

        # check whether the shortest line falls over the segment or outside the
        # segment
        # if - in segment then create a "hidden" node from the NODE
        # perpendicular to the line

        # else - connect to the closest node, whether its real NODE or "hidden"
        # node

        if theta_length < np.pi / 2:
            # the algorithm that does the perpendicular line
            # calculate gradients
            m1 = np.subtract(self.pointB.position.as_array, self.pointA.position.as_array)

            # add constant to remove any zero issues

            if not np.any(m1):
                m1 = np.add(m1, 1e-12)

            m1 = np.divide(m1[1], m1[0])
            if m1 == 0:
                m1 = np.add(1e-12, m1)

            m2 = np.divide(-1, m1)

            delta_m = np.subtract(m1, m2)

            x0 = (node.position.y - m2 * node.position.x + m1 * n1.position.x - n1.position.y) / delta_m
            y0 = node.position.y - (m2 * (node.position.x - x0))

            new_node = Node(position=Pos(x0, y0))
            new_node.isHidden = True

            ret_segment = Segment(new_node, node, new_node.distance_to(node))
            ret_segment.hasHidden = True
            return ret_segment
        else:
            # standard routing
            new_node = self.pointA
            # insures we do segment linking instead of pointless linking
            # forces conformity to the gained asset concept
            if not new_node.isHidden:
                ret_segment = Segment(self.pointB, node, self.pointB.distance_to(node))
                return ret_segment
            else:
                ret_segment = Segment(self.pointB, node, np.inf)
                return ret_segment
