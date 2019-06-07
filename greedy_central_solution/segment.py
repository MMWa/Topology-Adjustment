import numpy as np
import math

from simulation.node.Node import Node
from simulation.node.Pos import Pos


class segment:
    has_relays: bool
    has_hidden: bool

    def __init__(self, a: Node, b: Node, distance):
        self.point_a = a
        self.point_b = b
        self.distance = distance
        self.has_hidden = False
        self.has_relays = True

    @property
    def as_array(self):
        return [self.point_a, self.point_b]

    def distance_to(self, node: Node):
        dis_a = self.point_a.distance_to(node)
        dis_b = self.point_a.distance_to(self.point_b)
        dis_c = self.point_b.distance_to(node)

        if dis_a > dis_c:
            theta_length = (dis_b**2) + (dis_c**2) - (dis_a**2)
            try:
                theta_length = math.acos(theta_length / (2 * dis_b * dis_c))
            except:
                if (theta_length / (2 * dis_b * dis_c)) > 0:
                    theta_length = math.acos(1)
                else:
                    theta_length = math.acos(-1)
            n1 = self.point_a
        else:
            theta_length = (dis_b**2) + (dis_a**2) - (dis_c**2)
            try:
                theta_length = math.acos(theta_length / (2 * dis_b * dis_a))
            except:
                if (theta_length / (2 * dis_b * dis_a)) > 0:
                    theta_length = math.acos(1)
                else:
                    theta_length = math.acos(-1)

            n1 = self.point_b

        theta_length = abs(theta_length)

        # check whether the shortest line falls over the segment or outside the
        # segment
        # if - in segment then create a "hidden" node from the NODE
        # perpendicular to the line

        # else - connect to the closest node, whether its real NODE or "hidden"
        # node

        if theta_length < np.pi / 2:
            # the algorithm that does the perpendicular line
            # calculate gradients
            m1 = np.subtract(self.point_b.position.as_array, self.point_a.position.as_array)

            # add constant to remove any zero issues

            if not np.any(m1):
                m1 = m1 + 1e-8

            m1 = m1[1]/ m1[0]
            if m1 == 0:
                m1 = m1 + 1e-12

            m2 = -1/m1

            delta_m = m1-m2
            x0 = (node.position.y - m2 * node.position.x + m1 * n1.position.x - n1.position.y) / delta_m
            y0 = node.position.y - (m2 * (node.position.x - x0))

            new_node = Node(position=Pos(x0, y0))
            new_node.isHidden = True

            ret_segment = segment(new_node, node, new_node.distance_to(node))
            ret_segment.has_hidden = True
            return ret_segment

        else:
            if dis_a < dis_c:
                choosen = self.point_a
            else:
                choosen = self.point_b

            if not choosen.isHidden:
                return segment(choosen, node, choosen.distance_to(node))
            else:
                return segment(choosen, node, 1000000000000)
