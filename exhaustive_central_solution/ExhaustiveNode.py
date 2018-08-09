import numpy as np

from simulation.node import Node, Pos


class ExhaustiveNode(Node):
    def __init__(self, position:Pos = None, in_node:Node = None):

        if position is not None:
            super().__init__(position=position)
        elif in_node is not None:
            super().__init__()
            self = in_node

    def inside_box(self, a:Pos,b:Pos) -> bool:
        if a.x <= self.position.x <= b.x and a.y <= self.position.y <= b.y:
            return True
        else:
            return False

    def relative_quadrant(self, node:Node):
        angle = self.angle_to(target=node)
        pass
        # if angle != 0:
        #     if angle > 0:
        #         # to the right
        #     else:
        #         # to the left
        # else:
        #     # its on the line
        #
        # if ab


if __name__ == "__main__":
    node1 = ExhaustiveNode(position=Pos(0,0))

    for x in range(-5,5):
        for y in range(-5,5):
            node2 = ExhaustiveNode(position=Pos(x, y))
            print(str(x) +" - " + str(y) + " = " + str(node1.angle_to(node2) * 180 / np.pi))