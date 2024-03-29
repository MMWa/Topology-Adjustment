import math

from simulation.node.Pos import Pos

import numpy as np
from enum import Enum, auto
import uuid


class RegisterStates(Enum):
    passed = auto()
    connected = auto()
    no_state = auto()
    sending = auto()


class NodeType(Enum):
    Home = auto()
    End = auto()
    Relay = auto()


class Node:
    def __init__(self, position=None, internal_id=None):
        self.isHidden = False
        self.has_segment = 0
        self.__data = None
        self.type = NodeType.End

        if position is None:
            self.__position = Pos()
        else:
            self.__position = position

        if internal_id is not None:
            self.__ID = internal_id
        else:
            self.__ID = uuid.uuid1()

        self.Connection_List = []
        self.Connection_Count = 0
        self.test_register = RegisterStates.no_state

    def add_connection(self, u):
        self.Connection_List.append(u)
        self.Connection_Count += 1

    def update(self, x, y):
        self.position.x += x
        self.position.y += y

    # insure they cant be changed illegally
    @property
    def ID(self):
        return self.__ID

    @property
    def data(self):
        return self.__data

    def data_set(self):
        self.__data = True

    def data_clear(self):
        self.__data = True

    @property
    def position(self) -> Pos:
        return self.__position

    def distance_to(self, target) -> float:
        intermediate = np.subtract(self.position.as_array, target.position.as_array)
        intermediate = np.square(intermediate)
        intermediate = np.sum(intermediate)
        intermediate = np.sqrt(intermediate)
        return intermediate

    def angle_to(self, target) -> float:
        interm = np.subtract(target.position.as_array, self.position.as_array)
        return np.arctan2(interm[1], interm[0])

    def move_along_sin_rule(self, vector):
        self.position.x += vector[0]
        self.position.y += vector[1]

        print(self.position.as_array)

    def move_along_line(self, m, s):

        """

        :param m: angle of line
        :param s: length of line
        """

        x, y = self.position.as_array

        g = math.tan(m)

        g_factor = g ** 2
        g_factor = 1 + g_factor
        g_factor = math.sqrt(g_factor)

        x_o = 1 / g_factor
        x_o = s * x_o

        y_o = g / g_factor
        y_o = s * y_o

        if m > np.pi / 2 or m < - np.pi / 2:
            x_o = x - x_o
            y_o = y - y_o
        else:
            x_o = x + x_o
            y_o = y + y_o

        self.position.x = x_o
        self.position.y = y_o

    def __gt__(self, other):
        return np.greater(other.position.as_array, self.position.as_array)

    def __ge__(self, other):
        return not np.greater(self.position.as_array, other.position.as_array)

    def __le__(self, other):
        return not np.greater(other.position.as_array, self.position.as_array)


if __name__ == "__main__":
    # create with and without values
    node_test1 = Node()
    node_test2 = Node(Pos(34, 36), 4)

    # test values can be returned
    print(node_test1.position.x)
    print(node_test2.position.x)
    print(node_test2.position.as_array)

    # test distance to function
    print(node_test2.distance_to(node_test1))

    # test distance to self
    print(node_test1.distance_to(node_test1))
